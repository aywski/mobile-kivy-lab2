from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.uix.dropdown import DropDown
from kivy.uix.textinput import TextInput
from kivy_garden.mapview import MapView, MapMarker
from sqlalchemy.orm import sessionmaker
from screens.db_control import Student
from geopy.geocoders import Nominatim

class ContactScreen(Screen):
    def __init__(self, engine, **kwargs):
        super().__init__(**kwargs)
        self.engine = engine

        # Set up SQLAlchemy session
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Layout for the screen
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(self.layout)

        # Top buttons
        top_buttons = BoxLayout(orientation='horizontal', size_hint_y=0.1)
        self.student_dropdown = DropDown()
        self.student_button = Button(text='Show Location', size_hint_x=0.8)
        self.student_button.bind(on_press=self.show_location_by_id)
        
        # TextInput for ID
        self.id_input = TextInput(hint_text="Enter ID", size_hint_x=0.2)
        top_buttons.add_widget(self.id_input)
        top_buttons.add_widget(self.student_button)
        self.layout.add_widget(top_buttons)

        # MapView for displaying the map
        self.map_view = MapView(zoom=12, lat=50.4501, lon=30.5234)
        self.layout.add_widget(self.map_view)

        # List to keep track of markers
        self.markers = []

    def show_location_by_id(self, instance):
        # Retrieve the entered ID from the TextInput
        student_id = self.id_input.text

        if student_id.isdigit():
            # Try to find the student by ID
            student = self.session.query(Student).filter_by(id=int(student_id)).first()
            
            if student:
                # Show location if student is found
                self.show_location(student)
            else:
                # Show popup if student is not found
                self.show_error_popup("No student found with this ID.")
        else:
            self.show_error_popup("Please enter a valid ID.")

    def show_error_popup(self, message):
        # Show an error popup with the provided message
        popup_content = BoxLayout(orientation='vertical', spacing=10)
        error_label = Label(text=message)
        popup_content.add_widget(error_label)

        close_button = Button(text='Close', padding=(0, 10))
        close_button.bind(on_press=lambda x: popup.dismiss())
        popup_content.add_widget(close_button)

        popup = Popup(title='Error', content=popup_content, size_hint=(0.6, 0.4))
        popup.open()

    def show_location(self, student):
        # Remove existing markers
        for marker in self.markers:
            self.map_view.remove_marker(marker)
        self.markers.clear()

        # Retrieve student’s address
        student_address = student.address
        geolocator = Nominatim(user_agent="kivy_app")
        
        try:
            # Attempt to geocode the address
            location_info = geolocator.geocode(student_address)
            
            if location_info:
                # Get latitude and longitude
                student_lat, student_lon = location_info.latitude, location_info.longitude
                
                # Center the map on the student’s location
                self.map_view.center_on(student_lat, student_lon)
                
                # Add marker for student’s address
                student_marker = MapMarker(lat=student_lat, lon=student_lon)
                self.map_view.add_marker(student_marker)
                
                # Keep track of the marker
                self.markers.append(student_marker)
                
                # Update label with location info
                popup_content = BoxLayout(orientation='vertical', spacing=10)
                location_label = Label(text=f"Location Found:\nAddress: {student_address}\nCoordinates: ({student_lat}, {student_lon})")
                popup_content.add_widget(location_label)

                close_button = Button(text='Close', padding=(0, 10))
                close_button.bind(on_press=lambda x: popup.dismiss())
                popup_content.add_widget(close_button)

                popup = Popup(title='Student Location', content=popup_content, size_hint=(0.6, 0.4))
                popup.open()
            else:
                self.show_error_popup("Unable to geocode the student's address.")
        
        except Exception as e:
            self.show_error_popup(f"Error locating address: {str(e)}")
