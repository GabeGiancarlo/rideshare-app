# MySQL & Python Ride Share App
**CPSC408**

## Overview
Suppose that a new start-up is trying to create a rideshare app and hires you to design their database. Think about the main information that the app must keep track of and create some deliverables to show your client as you go.

## Deliverables
You and your optional partner must create:

1. **An ER diagram**
2. **A database schema** with all tables and attributes
3. **A database on MySQL** locally
4. **Sample data** within your database to test
5. **A simple interactive python program**

## Application Specifications

### User Authentication & Account Management

1. You will ask the user if they do not have an account, or if they are an existing rider or an existing driver.
2. If the user is new, let them create either a rider or driver account.
3. If the user is not new, have them log into a specific rider or driver account using some sort of an ID or username.

### Driver Features

If the user is a driver, you will give them the following options:

**a. View Rating**
   - This will show the driver their current rating
   - This will be the average rating of all rides they have given

**b. View Rides**
   - This will show the driver the list of all rides they have given

**c. Activate/Deactivate Driver Mode**
   - This updates a flag on their profile, letting riders know if they are accepting new rides right now

### Rider Features

If the user is a rider, you will give them the following options:

**a. View Rides**
   - This will show the rider the list of all rides they have taken

**b. Find a Driver**
   - Match the rider with a driver that has their driver mode activated
   - The rider will then provide the following info:
     1. Pick up location
     2. Drop off location
   - You will then create a ride and record that the driver drove that rider to the locations specified
   - You will then send the rider back to their options menu

**c. Rate My Driver**
   - You will look up the rider's most recent ride
   - You will then print the information of this ride to the user and ask if it is correct
   - If it is not the correct ride, you will have them enter the rideID of the ride they want to rate. Print that ride's information and have them confirm
   - Store the rating the rider gave on the ride record

## Database Design Guidelines

### Design Requirements

Any database schema you think can accomplish the above use case that is correctly normalized is allowed, as long as you can justify your design decisions to me. Feel free to add any more attributes or functionality on top of this as you see fit to make a good application to show your theoretical client!

### Planning Steps

Ensure you plan using the correct steps:

1. **Create your ER Diagram**
2. **Assign relationships** and then determine their cardinality
3. **Use referential integrity** and foreign keys to ensure you translate those relationships correctly into a schema
4. **Normalize to 3rd Normal Form** by identifying all functional dependencies, primary keys, and foreign keys
5. **Create your schema and database** + the app around it similar to how we built the playlist app

## Important Notes

You may come to me at any time asking to confirm your plan looks good before you implement it (and in fact I enthusiastically recommend it!). If you implement a non-normalized database, or a database where the foreign key placement does not match the relationships on your ER diagram, **I WILL make you redo it to get full points!** Better to ask me earlier instead of later :)

