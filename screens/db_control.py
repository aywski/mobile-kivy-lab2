from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput

from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# Student model for the database
class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    grade1 = Column(Float, nullable=False)
    grade2 = Column(Float, nullable=False)
    address = Column(String, nullable=True)

    @property
    def average_grade(self):
        return (self.grade1 + self.grade2) / 2


class StudentManagementScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical')
        self.add_widget(self.layout)

        # Top panel
        self.top_layout = BoxLayout(size_hint=(1, 0.2), orientation='vertical', padding=[5, 5, 5, 5], spacing=1)
        self.layout.add_widget(self.top_layout)

        # First row of buttons
        self.row1_layout = BoxLayout(size_hint=(1, 0.5), spacing=1)
        self.top_layout.add_widget(self.row1_layout)

        self.add_student_button = Button(text="Add Student")
        self.add_student_button.bind(on_press=self.show_add_student_popup)
        self.row1_layout.add_widget(self.add_student_button)

        self.delete_all_button = Button(text="Delete All Students")
        self.delete_all_button.bind(on_press=self.delete_all_students)
        self.row1_layout.add_widget(self.delete_all_button)

        # Second row of buttons
        self.row2_layout = BoxLayout(size_hint=(1, 0.5), spacing=1)
        self.top_layout.add_widget(self.row2_layout)

        self.percentage_button = Button(text="Calculate %")
        self.percentage_button.bind(on_press=self.calculate_percentage)
        self.row2_layout.add_widget(self.percentage_button)

        self.show_high_avg_button = Button(text="Show Students with Avg > 60")
        self.show_high_avg_button.bind(on_press=self.show_high_avg_students)
        self.row2_layout.add_widget(self.show_high_avg_button)

        # Main output area
        self.output_label = Label(size_hint=(1, 0.8))
        self.layout.add_widget(self.output_label)

        # Database setup
        self.engine = engine  # Using SQLite for simplicity
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.row3_layout = BoxLayout(size_hint=(1, 0.5), spacing=1)
        self.top_layout.add_widget(self.row3_layout)

        # Add the new button to the constructor
        self.show_all_button = Button(text="Show All Students")
        self.show_all_button.bind(on_press=self.show_all_students)
        self.row3_layout.add_widget(self.show_all_button)

        # New button for showing students with name "Іван"
        self.show_ivan_button = Button(text="Ivan")
        self.show_ivan_button.bind(on_press=self.show_ivan_students)
        self.row3_layout.add_widget(self.show_ivan_button)

    def show_all_students(self, instance):
        # Retrieve all students from the database
        students = self.session.query(Student).order_by(Student.name).all()

        # Create a container for displaying the list
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        if students:
            # Add students in the format ID: Name, Avg Grade
            for s in students:
                student_info = f"ID: {s.id}\nName: {s.name}\nAverage Grade: {s.average_grade:.2f}\nAddress: {s.address or 'Not specified'}"
                student_label = Label(
                    text=student_info,
                    size_hint_y=None,
                    height=100,
                    halign='left',
                    valign='middle',
                    text_size=(300, None)  # Set width for text adaptation
                )
                content.add_widget(student_label)
        else:
            # If the list is empty
            content.add_widget(Label(text="The student list is empty.", size_hint_y=None, height=100))

        # Add a "Close" button at the bottom
        close_button = Button(text="Close", size_hint_y=None, height=50)

        def close_popup(instance):
            popup.dismiss()

        close_button.bind(on_press=close_popup)
        content.add_widget(close_button)

        # Create a popup for displaying the list
        popup = Popup(
            title="Student List",
            content=content,
            size_hint=(0.9, 0.9),  # Popup will occupy 90% of the screen
            auto_dismiss=False
        )
        popup.open()

    def show_ivan_students(self, instance):
        # Retrieve students with name "Іван"
        ivan_students = self.session.query(Student).filter(Student.name == "Іван").all()

        # Create a container for displaying the list
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        if ivan_students:
            # Add students in the format ID: Name, Avg Grade
            for s in ivan_students:
                student_info = f"ID: {s.id}\nName: {s.name}\nAverage Grade: {s.average_grade:.2f}\nAddress: {s.address or 'Not specified'}"
                student_label = Label(
                    text=student_info,
                    size_hint_y=None,
                    height=100,
                    halign='left',
                    valign='middle',
                    text_size=(300, None)  # Set width for text adaptation
                )
                content.add_widget(student_label)
        else:
            # If no students named "Іван" are found
            content.add_widget(Label(text="No students named 'Іван' found.", size_hint_y=None, height=100))

        # Add a "Close" button at the bottom
        close_button = Button(text="Close", size_hint_y=None, height=50)

        def close_popup(instance):
            popup.dismiss()

        close_button.bind(on_press=close_popup)
        content.add_widget(close_button)

        # Create a popup for displaying the list of "Іван"
        popup = Popup(
            title="Students Named 'Іван'",
            content=content,
            size_hint=(0.9, 0.9),  # Popup will occupy 90% of the screen
            auto_dismiss=False
        )
        popup.open()

    def show_add_student_popup(self, instance):
        # Popup for adding a new student
        content = BoxLayout(orientation='vertical')
        name_input = TextInput(hint_text="Name")
        grade1_input = TextInput(hint_text="Grade 1")
        grade2_input = TextInput(hint_text="Grade 2")
        address_input = TextInput(hint_text="Address")
        add_button = Button(text="Add")

        def add_student(instance):
            name = name_input.text
            grade1 = float(grade1_input.text)
            grade2 = float(grade2_input.text)
            address = address_input.text

            new_student = Student(name=name, grade1=grade1, grade2=grade2, address=address)
            self.session.add(new_student)
            self.session.commit()
            popup.dismiss()
            self.output_label.text = "Student added!"

        content.add_widget(name_input)
        content.add_widget(grade1_input)
        content.add_widget(grade2_input)
        content.add_widget(address_input)
        content.add_widget(add_button)
        popup = Popup(title="Add Student", content=content, size_hint=(0.8, 0.8))
        add_button.bind(on_press=add_student)
        popup.open()

    def show_high_avg_students(self, instance):
        # Show students with an average grade > 60
        students = self.session.query(Student).all()
        high_avg_students = [s for s in students if s.average_grade > 60]
        if high_avg_students:
            self.output_label.text = "\n".join(
                f"{s.name} (Avg Grade: {s.average_grade:.2f})" for s in high_avg_students
            )
        else:
            self.output_label.text = "No students with Avg Grade > 60."

    def calculate_percentage(self, instance):
        # Calculate percentage of students with an average grade > 60
        students = self.session.query(Student).all()
        if not students:
            self.output_label.text = "No data for calculation."
            return
        high_avg_students = [s for s in students if s.average_grade > 60]
        percentage = (len(high_avg_students) / len(students)) * 100
        self.output_label.text = f"Percentage of students with Avg Grade > 60: {percentage:.2f}%."

    def delete_all_students(self, instance):
        # Clear the database (delete all students)
        self.session.query(Student).delete()
        self.session.commit()
        self.output_label.text = "All students deleted."
