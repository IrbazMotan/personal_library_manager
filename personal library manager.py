import streamlit as st
st.set_page_config(
    page_title="baba book", 
    page_icon="books.png",
    layout="wide"
)
# Initialize session state variables
if "show_fields" not in st.session_state:
    st.session_state.show_fields = False
if "show_delete" not in st.session_state:
    st.session_state.show_delete = False
if "show_books" not in st.session_state:
    st.session_state.show_books = False
if "show_search" not in st.session_state:
    st.session_state.show_search = False
if "search_query" not in st.session_state:
    st.session_state.search_query = ""
if "search_filter" not in st.session_state:
    st.session_state.search_filter = "Name"

# Function to add a book
def add_item():
    """Function to add a new book entry."""
    st.subheader("Add a New Book")
    with st.form(key="add_book_form"):
        name = st.text_input("Name")
        author = st.text_input("Author")
        publisher = st.text_input("Publisher")
        book_type = st.text_input("Type")

        submit = st.form_submit_button("Submit")
        if submit:
            if name and author and publisher and book_type:
                book_entry = f"{name},{author},{publisher},{book_type}\n"
                with open("plm.txt", "a") as file:
                    file.write(book_entry)
                st.success("Book added successfully!")
                st.session_state.show_fields = False
            else:
                st.warning("Please fill in all fields.")

# Function to delete a book
def delete_item():
    """Function to delete a selected book entry."""
    st.subheader("Delete a Book")
    try:
        with open("plm.txt", "r") as file:
            books = [line.strip() for line in file.readlines()]

        if not books:
            st.warning("No books available to delete.")
            return

        book_options = {i: book.split(",")[0] for i, book in enumerate(books)}
        selected_index = st.selectbox(
            "Select a book to delete:",
            options=book_options.keys(),
            format_func=lambda x: f"{x+1}. {book_options[x]}"
        )

        if st.button("Confirm Delete"):
            updated_books = [book for i, book in enumerate(books) if i != selected_index]
            with open("plm.txt", "w") as file:
                file.write("\n".join(updated_books) + "\n")
            st.success("Book deleted successfully!")
    except FileNotFoundError:
        st.error("File not found. Add a book first.")

# Function to display all books
def show_books():
    """Function to display all saved books."""
    st.subheader("Book List")
    try:
        with open("plm.txt", "r") as file:
            books = [line.strip().split(",") for line in file.readlines()]

        if not books:
            st.warning("No books available.")
            return

        for i, book in enumerate(books):
            if len(book) < 4:
                continue  # Skip incomplete entries
            name, author, publisher, book_type = book
            st.text(f"""
            **{i+1}. {name}**  
            Author: {author}  
            Publisher: {publisher}  
            Type: {book_type}
            """)
            # Add a delete button for each book
            delete_button = st.button(f"Delete {name}", key=f"delete_{i}")

            if delete_button:
                # Delete the book from the original list
                book_index = books.index(book)
                updated_books = [book for idx, book in enumerate(books) if idx != book_index]

                # Write the updated list back to the file
                with open("plm.txt", "w") as file:
                    file.write("\n".join([",".join(b) for b in updated_books]) + "\n")

                st.success(f"Book '{name}' deleted successfully!")

    except FileNotFoundError:
        st.error("No records found.")

# Function to search books (with delete option)
def search_books():
    """Function to search books by Name, Author, Publisher, or Type, and delete a book from the search results."""
    st.subheader("🔍 Search for a Book")

    search_query = st.text_input("Enter search text", value=st.session_state.search_query)
    search_filter = st.selectbox("Filter by:", ["Name", "Author", "Publisher", "Type"], index=["Name", "Author", "Publisher", "Type"].index(st.session_state.search_filter))

    if st.button("Search"):
        st.session_state.search_query = search_query.strip().lower()
        st.session_state.search_filter = search_filter

    if not st.session_state.search_query:
        return  # Don't show search results if search query is empty

    try:
        with open("plm.txt", "r") as file:
            books = [line.strip().split(",") for line in file.readlines()]

        if not books:
            st.warning("No books available.")
            return

        # Mapping filter to the correct index in book data
        filter_index = {"Name": 0, "Author": 1, "Publisher": 2, "Type": 3}[st.session_state.search_filter]

        # Filtering books based on search query and filter
        filtered_books = [
            book for book in books
            if len(book) >= 4 and st.session_state.search_query in book[filter_index].strip().lower()
        ]

        if not filtered_books:
            st.warning("No books match your search.")
            return

        # Display search results with a delete button
        st.subheader(f"📚 Search Results ({st.session_state.search_filter})")
        for i, book in enumerate(filtered_books):
            name, author, publisher, book_type = book
            st.text(f"""
            **{i+1}. {name}**  
            Author: {author}  
            Publisher: {publisher}  
            Type: {book_type}
            """)
            delete_button = st.button(f"Delete {name}", key=f"delete_{i}")

            if delete_button:
                # Delete the book from the original list
                book_index = books.index(book)
                updated_books = [book for idx, book in enumerate(books) if idx != book_index]

                # Write the updated list back to the file
                with open("plm.txt", "w") as file:
                    file.write("\n".join([",".join(b) for b in updated_books]) + "\n")

                st.success(f"Book '{name}' deleted successfully!")

    except FileNotFoundError:
        st.error("No records found. Please add books first.")

# Main UI
st.header("baba book library manager")

# Create a row with columns to place buttons side by side
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Add Book"):
        st.session_state.show_fields = True
        st.session_state.show_delete = False
        st.session_state.show_books = False
        st.session_state.show_search = False

# with col2:
#     if st.button("Delete Book"):
#         st.session_state.show_fields = False
#         st.session_state.show_delete = True
#         st.session_state.show_books = False
#         st.session_state.show_search = False

with col2:
    if st.button("Show Books"):
        st.session_state.show_fields = False
        st.session_state.show_delete = False
        st.session_state.show_books = True
        st.session_state.show_search = False

with col3:
    if st.button("Search Book"):
        st.session_state.show_fields = False
        st.session_state.show_delete = False
        st.session_state.show_books = False
        st.session_state.show_search = True

# Show the appropriate section
if st.session_state.show_fields:
    add_item()
# elif st.session_state.show_delete:
#     delete_item()
elif st.session_state.show_books:
    show_books()
elif st.session_state.show_search:
    search_books()
