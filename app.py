import mysql.connector


# -----------------------------
# DATABASE CONNECTION
# -----------------------------

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="YOUR_MYSQL_PASSWORD",
        database="blood_donation_db"
    )


# -----------------------------
# REGISTER DONOR
# -----------------------------

def register_donor():

    print("\n===== REGISTER DONOR =====")

    full_name = input("Enter full name: ")

    # Validate age
    while True:
        try:
            age = int(input("Enter age: "))

            if age < 18:
                print("Donor must be at least 18 years old.")
                return

            break

        except ValueError:
            print("Please enter a valid age.")

    # Blood group
    valid_blood_groups = [
        "A+", "A-", "B+", "B-",
        "O+", "O-", "AB+", "AB-"
    ]

    while True:
        blood_group = input("Enter blood group: ").upper()

        if blood_group in valid_blood_groups:
            break

        print("Invalid blood group. Please try again.")

    city = input("Enter city: ")
    phone = input("Enter phone number: ")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    INSERT INTO donors
    (full_name, age, blood_group, city, phone)
    VALUES (%s, %s, %s, %s, %s)
    """

    values = (full_name, age, blood_group, city, phone)

    cursor.execute(query, values)

    conn.commit()

    print("\nDonor registered successfully!")
    print("Donor ID:", cursor.lastrowid)

    cursor.close()
    conn.close()


# -----------------------------
# VIEW ALL AVAILABLE DONORS
# -----------------------------

def view_donors():

    print("\n===== AVAILABLE DONORS =====")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, full_name, age, blood_group, city
    FROM donors
    WHERE is_available = 1
    """

    cursor.execute(query)

    donors = cursor.fetchall()

    if len(donors) == 0:
        print("No available donors found.")

    else:
        print("\nID | Name | Age | Blood Group | City")
        print("-" * 50)

        for donor in donors:
            print(
                donor[0], "|",
                donor[1], "|",
                donor[2], "|",
                donor[3], "|",
                donor[4]
            )

    cursor.close()
    conn.close()


# -----------------------------
# SEARCH BY BLOOD GROUP
# -----------------------------

def search_by_blood_group():

    print("\n===== SEARCH DONOR =====")

    valid_blood_groups = [
        "A+", "A-", "B+", "B-",
        "O+", "O-", "AB+", "AB-"
    ]

    while True:
        blood_group = input("Enter blood group: ").upper()

        if blood_group in valid_blood_groups:
            break

        print("Invalid blood group.")

    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
    SELECT id, full_name, age, blood_group, city
    FROM donors
    WHERE blood_group = %s
    AND is_available = 1
    """

    cursor.execute(query, (blood_group,))

    donors = cursor.fetchall()

    if len(donors) == 0:
        print("\nNo available donors found for", blood_group)

    else:
        print("\nAvailable", blood_group, "donors:")
        print("\nID | Name | Age | Blood Group | City")
        print("-" * 50)

        for donor in donors:
            print(
                donor[0], "|",
                donor[1], "|",
                donor[2], "|",
                donor[3], "|",
                donor[4]
            )

    cursor.close()
    conn.close()


# -----------------------------
# CHANGE DONOR AVAILABILITY
# -----------------------------

def change_availability():

    print("\n===== CHANGE AVAILABILITY =====")

    try:
        donor_id = int(input("Enter donor ID: "))

    except ValueError:
        print("Invalid donor ID.")
        return

    conn = get_db_connection()
    cursor = conn.cursor()

    # First check current status
    cursor.execute(
        "SELECT full_name, is_available FROM donors WHERE id = %s",
        (donor_id,)
    )

    donor = cursor.fetchone()

    if donor is None:
        print("Donor not found.")

    else:
        current_status = donor[1]

        if current_status == 1:
            new_status = 0
            status_text = "unavailable"
        else:
            new_status = 1
            status_text = "available"

        cursor.execute(
            """
            UPDATE donors
            SET is_available = %s
            WHERE id = %s
            """,
            (new_status, donor_id)
        )

        conn.commit()

        print(
            donor[0],
            "is now marked as",
            status_text
        )

    cursor.close()
    conn.close()


# -----------------------------
# MAIN MENU
# -----------------------------

def main():

    while True:

        print("\n")
        print("=" * 40)
        print("   BLOOD DONATION MANAGEMENT SYSTEM")
        print("=" * 40)

        print("1. Register Donor")
        print("2. View Available Donors")
        print("3. Search Donor by Blood Group")
        print("4. Change Donor Availability")
        print("5. Exit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            register_donor()

        elif choice == "2":
            view_donors()

        elif choice == "3":
            search_by_blood_group()

        elif choice == "4":
            change_availability()

        elif choice == "5":
            print("\nThank you for using the system.")
            break

        else:
            print("\nInvalid choice. Please try again.")


# -----------------------------
# START PROGRAM
# -----------------------------

if __name__ == "__main__":
    main()