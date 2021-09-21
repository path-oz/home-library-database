from tkinter import *
import sqlite3

root = Tk()
root.title('My Library!')
root.geometry("400x400")


conn = sqlite3.connect("book_list.db")

c = conn.cursor()

#Create Table
#c.execute("""CREATE TABLE books (
        #title text,
        #author text,
        #isbn text,
        #rating integer
        #)""")

#Submit Function for Database

def delete():
    conn = sqlite3.connect("book_list.db")

    c = conn.cursor()

    c.execute("DELETE from books WHERE oid= " + delete_box.get())

    conn.commit()
    # Close Connection
    conn.close()

def submit():
    conn = sqlite3.connect("book_list.db")

    c = conn.cursor()

    #insert into table
    c.execute("INSERT INTO books VALUES (:title, :author, :isbn, :rating)",
              {
                 "title": title.get(),
                  "author": author.get(),
                  "isbn": isbn.get(),
                  "rating": rating.get()
              })

    conn.commit()
    # Close Connection
    conn.close()

    title.delete(0, END)
    author.delete(0, END)
    isbn.delete(0, END)
    rating.delete(0, END)

#edit function
def edit():
    global editor
    editor = Tk()
    editor.title('Update A Record')
    editor.geometry("400x400")

    conn = sqlite3.connect("book_list.db")

    c = conn.cursor()

    # Query the database
    book_id = delete_box.get()
    c.execute("SELECT * FROM books WHERE oid = " + book_id)
    books = c.fetchall()

    # Create blogabl Variables
    global title_editor
    global author_editor
    global isbn_editor
    global rating_editor

    # Create Text Boxes

    title_editor = Entry(editor, width=30)
    title_editor .grid(row=0, column=1, padx=20)

    author_editor  = Entry(editor, width=30)
    author_editor .grid(row=1, column=1, padx=20)

    isbn_editor  = Entry(editor, width=30)
    isbn_editor .grid(row=2, column=1, padx=20)

    rating_editor  = Entry(editor, width=30)
    rating_editor .grid(row=3, column=1, padx=20)

    # Create Text Boxes
    title_label = Label(editor, text="Title")
    title_label.grid(row=0, column=0)

    author_label = Label(editor, text="Author")
    author_label.grid(row=1, column=0)

    isbn_label = Label(editor, text="ISBN")
    isbn_label.grid(row=2, column=0)

    rating_label = Label(editor, text="Rate 1-10")
    rating_label.grid(row=3, column=0)

    # Loop through results
    for book in books:
        title_editor.insert(0, book[0])
        author_editor.insert(0, book[1])
        isbn_editor.insert(0, book[2])
        rating_editor.insert(0, book[3])


    # Create Save Button
    save_edit_button = Button(editor, bg='green', text="Update Book", command=update)
    save_edit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)


def update():
    conn = sqlite3.connect("book_list.db")

    c = conn.cursor()

    book_id = delete_box.get()

    c.execute("""UPDATE books SET
        title = :title,
        author = :author,
        isbn = :isbn,
        rating = :rating
        
        WHERE oid = :oid """,
        {"title":title_editor.get(),
         "author": author_editor.get(),
         "isbn": isbn_editor.get(),
         "rating": rating_editor.get(),

         "oid": book_id


        })

    conn.commit()
    # Close Connection
    conn.close()

    editor.destroy()





# Query Function
def query():

    conn = sqlite3.connect("book_list.db")

    c = conn.cursor()

    #Query the database
    c.execute("SELECT *, oid FROM books")
    books = c.fetchall()


    print_books = ""
    for book in books:
        print_books += str(book) + "\n"

    query_label = Label(root, text=print_books)
    query_label.grid(row=11, column=0, columnspan=2)
    conn.commit()
    # Close Connection
    conn.close()

# Create Text Boxes

title = Entry(root,width = 30)
title.grid(row=0, column=1, padx=20)

author = Entry(root,width = 30)
author.grid(row=1, column=1, padx=20)

isbn = Entry(root,width = 30)
isbn.grid(row=2, column=1, padx=20)

rating = Entry(root,width = 30)
rating.grid(row=3, column=1, padx=20)

# Delete Box

delete_box = Entry(root,width = 30)
delete_box.grid(row=9, column=1,)

# Create Text Boxes
title_label = Label(root, text="Title")
title_label.grid(row=0, column=0)

author_label = Label(root, text="Author")
author_label.grid(row=1, column=0)

isbn_label = Label(root, text="ISBN")
isbn_label.grid(row=2, column=0)

rating_label = Label(root, text="Rate 1-10")
rating_label.grid(row=3, column=0)


#Delete box label
delete_box_label = Label(root, text="Select ID")
delete_box_label.grid(row=9, column=0)

# Create update Button
edit_button = Button(root, bg = 'gray', text="Edit Book", command=edit)
edit_button.grid(row=12, column=0, columnspan=2, pady=10, padx=10,ipadx=100)

# Create Submit Button
submit_button = Button(root, bg = 'green', text="Add Book!", command=submit)
submit_button.grid(row=6, column=0, columnspan=2, pady=10, padx=10,ipadx=100)


# Create Query Button
query_button = Button(root, bg = 'white', text="Show Books!", command=query)
query_button.grid(row=7, column=0, columnspan=2, pady=10, padx=10, ipadx=95)

#Create Delete Button

delete_button = Button(root, bg = 'red', text="Delete Book", command=delete)
delete_button.grid(row=10, column=0, columnspan=2, pady=10, padx=10, ipadx=96)

conn.commit()
# Close Connection
conn.close()





root.mainloop()