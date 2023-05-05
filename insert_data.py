from datetime import datetime, timedelta
from random import choice, randint
from faker import Faker
from utils import create_session
from create import Office, Agent, AgentOffice, Seller, Listing, Buyer, Sale, Commission

fake = Faker()

def insert_offices(session, num_offices=10):
    """
    Insert offices data into the database
    
    Args:
        session: database session
        num_offices: number of offices to insert
    Returns:
        None
    """
    # loop through the number of offices to insert the data
    try:
        for _ in range(num_offices):
            office = Office(address=fake.address())
            session.add(office)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def insert_agents(session, num_agents=50):
    """
    Inserts a specified number of agents into the database with fake data.
    
    Args:
        session (Session): SQLAlchemy session object for interacting with the database.
        num_agents (int, optional): Number of agents to be inserted. Defaults to 50.
    """
    try:
        for _ in range(num_agents):
            agent = Agent(name=fake.name(), email=fake.email(), phone=fake.phone_number())
            session.add(agent)

            # Assign each agent to at least one office
            agent_id = session.query(Agent).order_by(Agent.id.desc()).first().id
            agent_office = AgentOffice(agent_id=agent_id, office_id=choice(session.query(Office).all()).id)
            session.add(agent_office)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def assign_agents_to_offices(session, num_assignments=100):
    """
    Assigns agents to offices by creating relationships in the AgentOffice table.
    
    Args:
        session (Session): SQLAlchemy session object for interacting with the database.
        num_assignments (int, optional): Number of assignments to create. Defaults to 100.
    """
    offices = session.query(Office).all()
    agents = session.query(Agent).all()
    try:
        for _ in range(num_assignments):
            agent_office = AgentOffice(agent_id=choice(agents).id, office_id=choice(offices).id)
            session.add(agent_office)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
        
def insert_listings(session, num_listings=200):
    """
    Inserts a specified number of listings into the database and assigns each listing to a seller, an agent, and an office.
    
    Args:
        session (Session): SQLAlchemy session object for interacting with the database.
        num_listings (int, optional): Number of listings to be inserted. Defaults to 200.
    """
    agents = session.query(Agent).all()
    try:
        sellers = [Seller(name=fake.name(), phone=fake.phone_number()) for _ in range(num_listings)]
        session.add_all(sellers)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    try:
        for idx in range(num_listings):
            listing_agent = choice(agents)
            office_id = session.query(AgentOffice).filter(AgentOffice.agent_id == listing_agent.id).first().office_id

            listing = Listing(
                seller_id=sellers[idx].id,
                bedrooms=randint(1, 5),
                bathrooms=randint(1, 4),
                listing_price=fake.random_number(digits=6, fix_len=True),
                zip_code=fake.zipcode(),
                date_of_listing=fake.date_between(start_date='-3y', end_date='today'),
                listing_agent_id=listing_agent.id,
                office_id=office_id,
            )
            session.add(listing)
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def insert_sales(session, num_sales=100):
    """
    Inserts a specified number of sales into the database and updates listing status, commission, and sale information.
    
    Args:
        session (Session): SQLAlchemy session object for interacting with the database.
        num_sales (int, optional): Number of sales to be inserted. Defaults to 100.
    """
    try:
        # initialize list of buyers
        buyers = [Buyer(name=fake.name(), phone=fake.phone_number()) for _ in range(num_sales)]
        # add buyers to database
        session.add_all(buyers)
        # commit changes to database
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)
    # get all listings that are not sold
    listings = session.query(Listing).filter(Listing.is_sold == 0).limit(num_sales).all()
    try:
        # loop through the number of sales to insert the data
        for idx, listing in enumerate(listings):
            # get the selling agent and office id
            selling_agent_id = listing.listing_agent_id
            office_id = listing.office_id
            # create a sale object
            sale = Sale(
                buyer_id=buyers[idx].id,
                sale_price=listing.listing_price,
                date_of_sale=fake.date_between(start_date=listing.date_of_listing, end_date='today'),
                selling_agent_id=selling_agent_id,
                office_id=office_id,
                listing_id=listing.id
            )
            # add sale to database
            session.add(sale)
            sale_id = session.query(Sale).order_by(Sale.id.desc()).first().id
            # update listing status
            listing.is_sold = 1
            # calculate commission amount
            commision_rate = get_commission_rate(sale.sale_price)
            commision_amount = sale.sale_price * commision_rate
            commision = Commission(agent_id = selling_agent_id, sale_id = sale_id, amount = commision_amount, date_of_commission = sale.date_of_sale)
            # add commission to database
            session.add(commision)
        # commit changes to database
        session.commit()
    except Exception as e:
        session.rollback()
        print(e)

def get_commission_rate(sale_price):
    """
    Determines the commission rate based on the sale price of a property.
    Args:
    sale_price (int): The sale price of the property.

    Returns:
        float: The commission rate based on the sale price.
    """
    # determine commission rate based on sale price
    if sale_price < 100000:
        return 0.10
    elif sale_price < 200000:
        return 0.075
    elif sale_price < 500000:
        return 0.06
    elif sale_price < 1000000:
        return 0.05
    else:
        return 0.04
    
def main():
    """
    Calls all functions to insert data into the database.
    """
    # create session with database
    session = create_session()
    
    # insert data
    insert_offices(session, num_offices=50)
    insert_agents(session, num_agents=250)
    assign_agents_to_offices(session, num_assignments=500)
    insert_listings(session, num_listings=1000)
    insert_sales(session, num_sales=500)

if __name__ == "__main__":
    # execute only if run as a script
    main()
