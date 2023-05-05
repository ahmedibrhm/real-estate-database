from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# initialize the Office table that will be used to store the office information
class Office(Base):
    """
    Office class representing the offices in the real estate database.

    Attributes:
        id (int): Primary key, uniquely identifies an office.
        address (str): Address of the office.
    """
    __tablename__ = 'offices'
    id = Column(Integer, primary_key=True)  # Define 'id' as primary key
    address = Column(String, nullable=False)  # Define 'address', cannot be null

    def __repr__(self):
        """
        String representation of the Office object.

        Returns:
            str: A formatted string with the Office's id and address.
        """
        # Format the string to include 'id' and 'address' attributes
        return f"Office(id={self.id}, address={self.address})"

# initialize the Agent table that will be used to store the agent information
class Agent(Base):
    """
    Agent class representing the real estate agents in the database.

    Attributes:
        id (int): Primary key, uniquely identifies an agent.
        name (str): Name of the agent.
        email (str): Email address of the agent.
        phone (str): Phone number of the agent.
    """
    __tablename__ = 'agents'
    id = Column(Integer, primary_key=True)  # Define 'id' as primary key
    name = Column(String, nullable=False)  # Define 'name', cannot be null
    email = Column(String, nullable=False)  # Define 'email', cannot be null
    phone = Column(String, nullable=False)  # Define 'phone', cannot be null

    def __repr__(self):
        """
        String representation of the Agent object.

        Returns:
            str: A formatted string with the Agent's id, name, email, and phone.
        """
        # Format the string to include 'id', 'name', 'email', and 'phone' attributes
        return f"Agent(id={self.id}, name={self.name}, email={self.email}, phone={self.phone})"

# initialize the AgentOffice table that will be used to store the agent-office relationship
class AgentOffice(Base):
    """
    AgentOffice class representing the relationship between agents and offices.
    
    Attributes:
        id (int): Primary key, uniquely identifies an agent-office relationship.
        agent_id (int): Foreign key, identifies the agent.
        office_id (int): Foreign key, identifies the office.
    """
    __tablename__ = 'agent_office' # Define the table name
    id = Column(Integer, primary_key=True) # Define 'id' as primary key
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False) # Define 'agent_id', cannot be null
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=False) # Define 'office_id', cannot be null

    def __repr__(self):
        """
        String representation of the AgentOffice object.
        
        Returns:
            str: A formatted string with the AgentOffice's id, agent_id, and office_id.
        """
        return f"AgentOffice(id={self.id}, agent_id={self.agent_id}, office_id={self.office_id})"
    
    
class Seller(Base):
    """
    Seller class representing the sellers in the database.
    
    Attributes:
        id (int): Primary key, uniquely identifies a seller.
        name (str): Name of the seller.
        phone (str): Phone number of the seller.
    """
    __tablename__ = 'sellers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    
    def __repr__(self):
        """
        String representation of the Seller object.
        
        Returns:
            str: A formatted string with the Seller's id, name, and phone.
        """
        return f"Seller(id={self.id}, name={self.name}, phone={self.phone})"

class Listing(Base):
    """
    Listing class representing the listings in the database.
    
    Attributes:
        id (int): Primary key, uniquely identifies a listing.
        seller_id (int): Foreign key, identifies the seller.
        bedrooms (int): Number of bedrooms in the listing.
        bathrooms (int): Number of bathrooms in the listing.
        listing_price (float): Price of the listing.
        zip_code (str): Zip code of the listing.
        date_of_listing (date): Date the listing was created.
        listing_agent_id (int): Foreign key, identifies the listing agent.
        office_id (int): Foreign key, identifies the office.
        is_sold (int): Indicates if the listing is sold.
    """
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    seller_id = Column(Integer, ForeignKey('sellers.id'), nullable=False)
    bedrooms = Column(Integer, nullable=False)
    bathrooms = Column(Integer, nullable=False)
    listing_price = Column(Float, nullable=False)
    zip_code = Column(String, nullable=False)
    date_of_listing = Column(Date, nullable=False)
    listing_agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=False)
    is_sold = Column(Integer, nullable=False, default=0)
    
    def __repr__(self):
        """
        String representation of the Listing object.
        
        Returns:
            str: A formatted string with the Listing's id, seller_id, bedrooms, bathrooms, listing_price, zip_code, date_of_listing, listing_agent_id, office_id, and is_sold.
        """
        return f"Listing(id={self.id}, seller_id={self.seller_id}, bedrooms={self.bedrooms}, bathrooms={self.bathrooms}, listing_price={self.listing_price}, zip_code={self.zip_code}, date_of_listing={self.date_of_listing}, listing_agent_id={self.listing_agent_id}, office_id={self.office_id}, is_sold={self.is_sold})"

class Buyer(Base):
    """
    Buyer class representing the buyers in the database.
    
    Attributes:
        id (int): Primary key, uniquely identifies a buyer.
        name (str): Name of the buyer.
        phone (str): Phone number of the buyer.
    """
    __tablename__ = 'buyers'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    
    def __repr__(self):
        """
        String representation of the Buyer object.
        
        Returns:
            str: A formatted string with the Buyer's id, name, and phone.
        """
        return f"Buyer(id={self.id}, name={self.name}, phone={self.phone})"

class Sale(Base):
    """
    Sale class representing the sales in the database.
    
    Attributes:
        id (int): Primary key, uniquely identifies a sale.
        buyer_id (int): Foreign key, identifies the buyer.
        sale_price (float): Price of the sale.
        date_of_sale (date): Date the sale was created.
        selling_agent_id (int): Foreign key, identifies the selling agent.
        office_id (int): Foreign key, identifies the office.
        listing_id (int): Foreign key, identifies the listing.
    """
    __tablename__ = 'sales'
    id = Column(Integer, primary_key=True)
    buyer_id = Column(Integer, ForeignKey('buyers.id'), nullable=False)
    sale_price = Column(Float, nullable=False)
    date_of_sale = Column(Date, nullable=False)
    selling_agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    office_id = Column(Integer, ForeignKey('offices.id'), nullable=False)
    listing_id = Column(Integer, ForeignKey('listings.id'), nullable=False)
    
    def __repr__(self):
        """
        string representation of the Sale object.
        
        Returns:
            str: A formatted string with the Sale's id, buyer_id, sale_price, date_of_sale, selling_agent_id, office_id, and listing_id.
        """
        return f"Sale(id={self.id}, buyer_id={self.buyer_id}, sale_price={self.sale_price}, date_of_sale={self.date_of_sale}, selling_agent_id={self.selling_agent_id}, office_id={self.office_id}, listing_id={self.listing_id})"

class Commission(Base):
    """
    Commission class representing the commissions in the database based on each sale.
    
    Attributes:
        id (int): Primary key, uniquely identifies a commission.
        agent_id (int): Foreign key, identifies the agent.
        sale_id (int): Foreign key, identifies the sale.
        amount (float): Amount of the commission.
        date_of_commission (date): Date the commission was created.
    """
    __tablename__ = 'commissions'
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    sale_id = Column(Integer, ForeignKey('sales.id'), nullable=False)
    amount = Column(Float, nullable=False)
    date_of_commission = Column(Date, nullable=False)
    
    def __repr__(self):
        """
        string representation of the Commission object.
        
        Returns:
            str: A formatted string with the Commission's id, agent_id, sale_id, amount, and date_of_commission.
        """
        return f"Commission(id={self.id}, agent_id={self.agent_id}, sale_id={self.sale_id}, amount={self.amount}, date_of_commission={self.date_of_commission})"

class MonthlyCommission(Base):
    """
    MonthlyCommission class representing the monthly commissions for agents in the database.
    
    Attributes:
        id (int): Primary key, uniquely identifies a monthly commission.
        agent_id (int): Foreign key, identifies the agent.
        date (date): Date of the monthly commission.
        amount (float): Amount of the monthly commission.
    """
    __tablename__ = 'month_commissions'
    id = Column(Integer, primary_key=True)
    agent_id = Column(Integer, ForeignKey('agents.id'), nullable=False)
    date = Column(Date, nullable=False)
    amount = Column(Float, nullable=False)
    
    def __repr__(self):
        """
        String representation of the MonthlyCommission object.
        
        Returns:
            str: A formatted string with the MonthlyCommission's id, agent_id, date, and amount.
        """
        return f"MonthCommission(id={self.id}, agent_id={self.agent_id}, date={self.date}, amount={self.amount})"


# Indexes are used to speed up queries

# Create an index named 'idx_listing_agent_id' on the 'listing_agent_id' column of the 'Listing' table
Index('idx_listing_agent_id', Listing.listing_agent_id)

# Create an index named 'idx_selling_agent_id' on the 'selling_agent_id' column of the 'Sale' table
Index('idx_selling_agent_id', Sale.selling_agent_id)

# Create an index named 'idx_agent_id' on the 'agent_id' column of the 'Commission' table
Index('idx_agent_id', Commission.agent_id)

# Create an index named 'idx_sale_id' on the 'sale_id' column of the 'Commission' table
Index('idx_sale_id', Commission.sale_id)

# Create an index named 'idx_office_id_listing' on the 'office_id' column of the 'Listing' table
Index('idx_office_id_listing', Listing.office_id)

# Create an index named 'idx_office_id_sale' on the 'office_id' column of the 'Sale' table
Index('idx_office_id_sale', Sale.office_id)

# Create an index named 'date_of_listing' on the 'date_of_listing' column of the 'Listing' table
Index('date_of_listing', Listing.date_of_listing)

# Create an index named 'date_of_sale' on the 'date_of_sale' column of the 'Sale' table
Index('date_of_sale', Sale.date_of_sale)


# Create the database
engine = create_engine('sqlite:///real_estate.db', echo=True)
Base.metadata.create_all(engine)
