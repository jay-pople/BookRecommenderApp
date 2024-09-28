import mysql.connector as connector

class account_manager:

    def sign_in(self, name, password):
        con = connector.connect(
            host='localhost',
            user='root',
            passwd='0000',
            database="recommenderSystem"
        )
        query = "SELECT count(*) FROM user WHERE Name=%s AND Password=%s"
        params = (name, password)

        try:
            cursor = con.cursor()  # Initialize the cursor
            cursor.execute(query, params)
            result = cursor.fetchone()[0]  # Get the count
            cursor.close()  # Close the cursor
            con.close()  # Close the connection
            if result == 1:
                return 1  # Success
            else:
                return 0  # Failure (no matching user)
        except Exception as e:
            print(f"Error during sign-in: {e}")
            return 0  # Failure

    def sign_up(self, name, password):
        con = connector.connect(
            host='localhost',
            user='root',
            passwd='0000',
            database="recommenderSystem"
        )
        query = "INSERT INTO user (Name, Password) VALUES (%s, %s)"

        try:
            cursor = con.cursor()
            cursor.execute(query, (name, password))
            con.commit()  # Commit the transaction to save the changes
            cursor.close()
            con.close()
            return 1  # Success
        except Exception as e:
            con.rollback()  # Rollback in case of error
            print(f"Error during sign-up: {e}")
            return 0  # Failure
