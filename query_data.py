from sqlalchemy import func, and_, Date, cast
from utils import create_session
from create import Agent, Sale, MonthlyCommission, Office, Listing, Commission
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from tabulate import tabulate

def print_monthly_commission_table(year, month, session):
    # Define the date range for the given month
    start_date = datetime(year, month-1, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    # Query the MonthlyCommission table for the given month
    monthly_commissions = session.query(
        MonthlyCommission.agent_id,
        MonthlyCommission.amount
    ).filter(
        and_(
            MonthlyCommission.date >= start_date,
            MonthlyCommission.date < end_date
        )
    ).all()

    # Prepare table data and headers
    table_data = []
    headers = ["Agent ID", "Total Commission"]

    # Populate table data
    for monthly_commission in monthly_commissions:
        agent_id = monthly_commission.agent_id
        total_commission = monthly_commission.amount
        table_data.append([agent_id, total_commission])

    # Use tabulate to create and print the table
    table = tabulate(table_data, headers, tablefmt="grid")
    print(table)

def get_total_commission(year, month, session):
    """
    Calculates the total commission for each agent in a given month and stores it in the MonthlyCommission table.

    Args:
        year (int): The year for which the commission is calculated.
        month (int): The month for which the commission is calculated.
    """

    # Define the date range for the given month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    # Query the total commission for each agent in the given month
    agents_commission = session.query(
        Agent.id, func.sum(Commission.amount).label('total_commission')
    ).join(Commission, Commission.agent_id == Agent.id)\
    .filter(and_(Commission.date_of_commission >= start_date, Commission.date_of_commission < end_date))\
    .group_by(Agent.id)\
    .order_by(func.sum(Commission.amount).desc())\
    .all()


    # Add the monthly commission records to the MonthlyCommission table
    for agent_commission in agents_commission:
        if len(session.query(MonthlyCommission).filter(MonthlyCommission.agent_id == agent_commission[0], MonthlyCommission.date == end_date).all()) > 0:
            continue
        monthly_commission = MonthlyCommission(agent_id=agent_commission[0], date=end_date, amount=agent_commission[1])
        session.add(monthly_commission)
    
    session.commit()

def top_offices_by_sales_monthly(year, month, session):
    """
    Returns the top 5 offices by sales for a given month.

    Args:
        year (int): The year for which the sales are calculated.
        month (int): The month for which the sales are calculated.

    Returns:
        table: A table containing office id, address, and sales count.
    """

    # Define the date range for the given month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)

    # Query the top 5 offices by sales for the given month
    results = session.query(
        Office.id,
        Office.address,
        func.count(Sale.id).label('sales_count')
    ).join(Listing, Listing.office_id == Office.id)\
    .join(Sale, Sale.listing_id == Listing.id)\
    .filter(and_(Sale.date_of_sale >= start_date, Sale.date_of_sale < end_date))\
    .group_by(Office.id)\
    .order_by(func.count(Sale.id).desc())\
    .limit(5)\
    .all()

    session.close()

    return results


def top_agents_by_sales_monthly(year, month, session):
    """
    Returns the top 5 agents by sales for a given month.

    Args:
        year (int): The year for which the sales are calculated.
        month (int): The month for which the sales are calculated.

    Returns:
        table: A table containing agent id, name, email, phone, and sales count.
    """
    
    # Define the date range for the given month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    # Query the top 5 agents by sales for the given month
    results = session.query(
        Agent.id,
        Agent.name,
        Agent.email,
        Agent.phone,
        func.count(Sale.id).label('sales_count')
    ).join(Sale, Sale.selling_agent_id == Agent.id)\
    .filter(and_(Sale.date_of_sale >= start_date, Sale.date_of_sale < end_date))\
    .group_by(Agent.id)\
    .order_by(func.count(Sale.id).desc())\
    .limit(5)\
    .all()

    session.close()
    
    return results

def average_days_on_market_monthly(year, month, session):
    """
    Returns the average number of days a listing is on the market for a given month.

    Args:
        year (int): The year for which the average is calculated.
        month (int): The month for which the average is calculated.

    Returns:
        float: The average number of days on market for the given month.
    """

    # Define the date range for the given month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    # Query the average number of days on market for the given month
    results = session.query(
        func.avg(func.julianday(Sale.date_of_sale) - func.julianday(Listing.date_of_listing)).label('avg_days_on_market')
    ).join(Listing, Listing.id == Sale.listing_id)\
    .filter(and_(Sale.date_of_sale >= start_date, Sale.date_of_sale < end_date))\
    .scalar()
    session.close()
    return results

def average_selling_price_monthly(year, month, session):
    """
    Returns the average selling price of listings for a given month.

    Args:
        year (int): The year for which the average is calculated.
        month (int): The month for which the average is calculated.

    Returns:
        float: The average selling price for the given month.
    """
    # Define the date range for the given month
    start_date = datetime(year, month, 1)
    if month == 12:
        end_date = datetime(year + 1, 1, 1)
    else:
        end_date = datetime(year, month + 1, 1)
    # Query the average selling price for the given month
    results = session.query(
        func.avg(Sale.sale_price).label('avg_selling_price')
    ).filter(and_(Sale.date_of_sale >= start_date, Sale.date_of_sale < end_date))\
    .scalar()

    session.close()
    return results

def main():
    year, month = 2023, 4  # Change this to test different months
    # Calculate and store total commission for each agent for the given month
    
    get_total_commission(year, month, create_session())
    print("\n----------------------------------------")
    print("\nMonthly Report:")
    print("\n----------------------------------------")
    print("\nTop 5 Offices by Sales:")
    offices = top_offices_by_sales_monthly(year, month, create_session())
    table_offices = tabulate(offices, headers=['Office ID', 'Address', 'Sales Count'], tablefmt='grid')
    print(table_offices)
    # Display top 5 offices by sales for the given month
    print("\n----------------------------------------")
    print("\nTop 5 Agents by Sales:")
    agents = top_agents_by_sales_monthly(year, month, create_session())
    table_agents = tabulate(agents, headers=['Agent ID', 'Name', 'Email', 'Phone', 'Sales Count'], tablefmt='grid')
    print(table_agents)
    # Display average days on market for the given month
    print("\n----------------------------------------")
    print("\n Agents' Monthly Commissions:")
    print_monthly_commission_table(year, month+1, create_session())
    avg_days_on_market = average_days_on_market_monthly(year, month, create_session())
    print("\n----------------------------------------")
    print(f"\nAverage days on market for {year}-{month}: {avg_days_on_market} days")
    # Display average selling price for the given month
    avg_selling_price = average_selling_price_monthly(year, month, create_session())
    print("\n----------------------------------------")
    print(f"\nAverage selling price for {year}-{month}: ${avg_selling_price:.2f}")
    print("\n----------------------------------------")

if __name__ == "__main__":
    main()
