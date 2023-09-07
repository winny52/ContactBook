
from tabulate import tabulate
from models import EmailAddress,PhoneNumber,Contact,SessionLocal,initialize_database
from sqlalchemy import or_


def add_contact(session, first_name, last_name, address, phone_number, phone_id, email_address, email_type):
    try:
        
        new_contact = Contact(
            first_name=first_name,
            last_name=last_name,
            address=address
        )

        
        new_phone_number = PhoneNumber(
            phone_number=phone_number,
            phone_id=phone_id
        )
        new_contact.phone_numbers.append(new_phone_number)

        
        new_email_address = EmailAddress(
            email_address=email_address,
            email_type=email_type
        )
        new_contact.email_addresses.append(new_email_address)

        
        session.add(new_contact)
        session.commit()
        print("Contact added successfully.")
    except ValueError:
        print("Invalid input. Please check your input data.")


def view_contacts(session):
    try:
        
        contacts = session.query(Contact).all()

        if contacts:
            headers = ["ID", "First Name", "Last Name", "Address", "Phone Number", "Phone ID", "Email Address", "Email Type"]
            contact_data = []

            for contact in contacts:
                
                phone_number_data = "N/A"
                phone_id_data = "N/A"
                email_address_data = "N/A"
                email_type_data = "N/A"

            
                if contact.phone_numbers:
                    phone_number_data = contact.phone_numbers[0].phone_number
                    phone_id_data = contact.phone_numbers[0].phone_id

                if contact.email_addresses:
                    email_address_data = contact.email_addresses[0].email_address
                    email_type_data = contact.email_addresses[0].email_type

                contact_data.append((
                    contact.id,
                    contact.first_name,
                    contact.last_name,
                    contact.address,
                    phone_number_data,
                    phone_id_data,
                    email_address_data,
                    email_type_data
                ))

            print(tabulate(contact_data, headers, tablefmt="grid"))
        else:
            print("No contacts found.")
    except Exception as e:
        print(f"Error fetching and displaying contacts: {e}")


def edit_contact(session, contact_id, new_first_name, new_last_name, new_address, new_phone_number, new_phone_id, new_email_address, new_email_type):
    try:
        
        contact = session.query(Contact).filter(Contact.id == contact_id).first()
        if contact:
            
            contact.first_name = new_first_name
            contact.last_name = new_last_name
            contact.address = new_address
            
            
            if contact.phone_numbers:
                
                contact.phone_numbers[0].phone_number = new_phone_number
                contact.phone_numbers[0].phone_id = new_phone_id
            else:
                
                new_phone_number_obj = PhoneNumber(phone_number=new_phone_number, phone_id=new_phone_id)
                contact.phone_numbers.append(new_phone_number_obj)

            if contact.email_addresses:
                
                contact.email_addresses[0].email_address = new_email_address
                contact.email_addresses[0].email_type = new_email_type
            else:
                
                new_email_address_obj = EmailAddress(email_address=new_email_address, email_type=new_email_type)
                contact.email_addresses.append(new_email_address_obj)

            session.commit()
            print("Contact updated successfully.")
        else:
            print("Contact not found.")
    except Exception as e:
        print(f"Error editing contact: {e}")

def search_contacts(session, search_query):
    try:
        
        contacts = session.query(Contact).filter(
            or_(
                Contact.first_name.ilike(f"%{search_query}%"),
                Contact.last_name.ilike(f"%{search_query}%")
            )
        ).all()

        if contacts:
            headers = ["ID", "First Name", "Last Name", "Address", "Phone Number", "Phone ID", "Email Address", "Email Type"]
            contact_data = []

            for contact in contacts:
                phone_number_data = contact.phone_numbers[0] if contact.phone_numbers else None
                email_address_data = contact.email_addresses[0] if contact.email_addresses else None

                contact_data.append((
                    contact.id,
                    contact.first_name,
                    contact.last_name,
                    contact.address,
                    phone_number_data.phone_number if phone_number_data else None,
                    phone_number_data.phone_id if phone_number_data else None,
                    email_address_data.email_address if email_address_data else None,
                    email_address_data.email_type if email_address_data else None
                ))

            print(tabulate(contact_data, headers, tablefmt="fancy_grid"))
        else:
            print(f"No contacts found matching '{search_query}'.")
    except Exception as e:
        print(f"Error searching contacts: {e}")
def delete_contact(session, contact_id):
    contact = session.query(Contact).filter(Contact.id == contact_id).first()
    if contact:
        session.delete(contact)
        session.commit()
        print("Contact deleted successfully.")
    else:
        print("Contact not found.")

def main():
    
    initialize_database()

    
    session = SessionLocal()

    while True:
        print("\nContact Management Application")
        print("1. Add Contact")
        print("2. View Contacts")
        print("3. Edit Contact")
        print("4. Delete Contact")
        print("5. Search Contact")
        print("6. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            
            first_name = input("Enter first name: ")
            last_name = input("Enter last name: ")
            address = input("Enter address: ")
            phone_number = input("Enter Phone Number: ")
            phone_id = input("Enter Phone ID: ")
            email_address = input("Enter Email Address: ")
            email_type = input("Enter Email Type: ")
            add_contact(session, first_name, last_name, address, phone_number, phone_id, email_address, email_type)
           
        elif choice == "2":
            view_contacts(session)

        elif choice == "3":
            contact_id = int(input("Enter contact ID to edit: "))
            new_first_name = input("Enter new first name: ")
            new_last_name = input("Enter new last name: ")
            new_address = input("Enter new address: ")
            new_phone_number = input("Enter new Phone Number: ")
            new_phone_id = input("Enter new Phone ID: ")
            new_email_address = input("Enter new Email Address: ")
            new_email_type = input("Enter new Email Type: ")
            edit_contact(session, contact_id, new_first_name, new_last_name, new_address, new_phone_number, new_phone_id, new_email_address, new_email_type)

        elif choice == "4":
            contact_id = int(input("Enter contact ID to delete: "))
            delete_contact(session, contact_id)
            
        elif choice == "5":
            search_query = input("Enter a name to search for: ")
            search_contacts(session, search_query)
        elif choice == "6":
            session.close()
            break

if __name__ == "__main__":
    main()