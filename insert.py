from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from models import Category, Status, Priority, AvailableActivities


engine = create_engine("sqlite:///todo.db")
Session = sessionmaker(autocommit=False, expire_on_commit=False, bind=engine)
session = Session()


""" Insert pre-defined categories """

addDefault = Category(category_name="Default")
session.add(addDefault)

addPersonal = Category(category_name="Personal")
session.add(addPersonal)

addShopping = Category(category_name="Shopping")
session.add(addShopping)

addWishlist = Category(category_name="Wishlist")
session.add(addWishlist)

addWork = Category(category_name="Work")
session.add(addWork)


""" Insert pre-defined priorities """

addHigh = Priority(priority_name="High")
session.add(addHigh)

addMedium = Priority(priority_name="Medium")
session.add(addMedium)

addLow = Priority(priority_name="Low")
session.add(addLow)


""" Insert pre-defined status """

addOngoing = Status(status_name="Ongoing")
session.add(addOngoing)

addCompleted = Status(status_name="Completed")
session.add(addCompleted)


""" Insert pre-defined activities """

addActivity = AvailableActivities(activity_name="added")
session.add(addActivity)

updateActivity = AvailableActivities(activity_name="updated")
session.add(updateActivity)

session.commit()