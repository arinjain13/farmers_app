import requests
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.image import Image
from kivy.uix.filechooser import FileChooserIconView
from kivy.lang import Builder
from kivy.uix.checkbox import CheckBox
from kivy.uix.popup import Popup
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty



# KV Layout as a string
KV = '''
<InitialScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [500, 500, 500, 300]
        spacing: 30

        Label:
            text: "Welcome to the Farmer's Market App"
            font_size: 55

        Button:
            text: 'Login'
            on_press: root.manager.current = 'login'

        Button:
            text: 'Register'
            on_press: root.manager.current = 'register_choice'




<RegisterChoiceScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [300, 300, 300, 70]
        spacing: 15

        Label:
            text: "Register"
            font_size: 90

        TextInput:
            id: username
            hint_text: 'Username'
            font_size: 45
            size_hint_y: None
            height: 80

        TextInput:
            id: password
            hint_text: 'Password'
            font_size: 45
            password: True
            size_hint_y: None
            height: 80

        BoxLayout:
            orientation: 'horizontal'
            spacing: 20

            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Farmer'
                ColoredCheckBox:
                    id: farmer_checkbox
                    group: 'user_type'
                    background_color: (0, 0, 0, 1)  # Gray background color
                    color: (1, 1, 1, 1)  # Color of the checkmark
                    on_active: root.on_checkbox_active(self, self.active)

            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Consumer'
                ColoredCheckBox:
                    id: consumer_checkbox
                    group: 'user_type'
                    background_color: (0, 0, 0, 1)  # Gray background color
                    color: (1, 1, 1, 1)  # Color of the checkmark
                    on_active: root.on_checkbox_active(self, self.active)


        Button:
            text: 'Register'
            height: 40
            size_hint_x: None
            size_hint_y: None
            width: 500
            height: 100
            pos: (500, 500)
            on_press: root.register()

        Label:
            id: status_label
            text: ''
        
        Button:
            text: 'Back'
            height: 40
            size_hint_x: None
            size_hint_y: None
            width: 200
            height: 50
            pos: (100, 100)
            on_press: root.manager.current = 'initial'

<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [300, 300, 300, 70]
        spacing: 15

        Label:
            text: "Login"
            font_size: 90

        TextInput:
            id: username
            hint_text: 'Username'
            font_size: 45
            size_hint_y: None
            height: 80

        TextInput:
            id: password
            hint_text: 'Password'
            font_size: 45
            password: True
            size_hint_y: None
            height: 80

        BoxLayout:
            orientation: 'horizontal'
            spacing: 20

            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Farmer'
                ColoredCheckBox:
                    id: farmer_checkbox
                    group: 'user_type'
                    background_color: (0, 0, 0, 1)  # Gray background color
                    color: (1, 1, 1, 1)  # Color of the checkmark
                    on_active: root.on_checkbox_active(self, self.active)

            BoxLayout:
                orientation: 'horizontal'
                Label:
                    text: 'Consumer'
                ColoredCheckBox:
                    id: consumer_checkbox
                    group: 'user_type'
                    background_color: (0, 0, 0, 1)  # Gray background color
                    color: (1, 1, 1, 1)  # Color of the checkmark
                    on_active: root.on_checkbox_active(self, self.active)

        Button:
            text: 'Login'
            height: 40
            size_hint_x: None
            size_hint_y: None
            width: 500
            height: 100
            pos: (500, 500)
            on_press: root.login()

        Label:
            id: status_label
            text: ''

        Button:
            text: 'Back'
            height: 40
            size_hint_x: None
            size_hint_y: None
            width: 200
            height: 50
            pos: (100, 100)
            on_press: root.manager.current = 'initial'



<FarmerScreen>:
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: "Enlist Product"
            font_size: 90
        TextInput:
            id: product_name_input
            hint_text: 'Product Name'
            size_hint_y: None
            height: 80

        TextInput:
            id: product_description_input
            hint_text: 'Product Description'
            size_hint_y: None
            height: 250
            multiline: True

        TextInput:
            id: product_price_input
            hint_text: 'Product Price'
            size_hint_y: None
            height: 100

        Button:
            text: 'Upload Image'
            size_hint_y: None
            height: 60
            on_press: root.open_file_chooser(self)

        Image:
            id: image_display
            size_hint_y: None
            height: 200

        Button:
            text: 'Save Product'
            size_hint_y: None
            height: 60
            on_press: root.save_product(self)

        Label:
            id: status_label
            text: ''
            size_hint_y: None
            height: 40

        Button:
            text: 'Back'
            size_hint_y: None
            height: 60
            on_press: root.manager.current = 'initial'

            # Add logic for navigating back if needed

<ConsumerScreen>:
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: "Farm Connect"
            font_size: 110

        Button:
            text: 'Refresh Products'
            size_hint_y: None
            height: 40
            on_press: root.refresh_products()

        ScrollView:
            size_hint: (1, None)
            height: 200
            BoxLayout:
                id: product_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height  # Dynamically adjust the height

        Label:
            id: product_detail_label
            text: 'Product Details: '
            size_hint_y: None
            height: 100

        Button:
            id: add_to_cart_button
            text: 'Add to Cart'
            size_hint_y: None
            height: 50

        Label:
            id: status_label
            text: ''
            size_hint_y: None
            height: 50  # Display the status message here
    
        Button:
            text: 'View Cart'
            size_hint_y: None
            height: 50
            on_press: root.view_cart(self)
        
        Button:
            text: 'Back'
            size_hint_y: None
            height: 60
            on_press: root.manager.current = 'initial'


<OrderTrackingScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: [10, 10, 10, 10]
        spacing: 10

        TextInput:
            id: order_id_input
            hint_text: 'Enter Order ID'
            size_hint_y: None
            height: 30

        Button:
            text: 'Track Order'
            on_press: root.track_order()

        Label:
            id: status_label
            text: 'Order Status: '

        Button:
            text: 'Back'
            size_hint_y: None
            height: 40
            on_press: root.manager.current = 'initial'

<CartScreen>:
    BoxLayout:
        orientation: 'vertical'

        Label:
            text: "Cart"
            font_size: 110


        ScrollView:
            size_hint: (1, None)
            height: 300
            BoxLayout:
                id: cart_list
                orientation: 'vertical'
                size_hint_y: None
                height: self.minimum_height

        Label:
            id: total_label
            text: 'Total: $0.00'
            size_hint_y: None
            height: 40

        Button:
            text: 'Checkout'
            size_hint_y: None
            height: 40
            on_press: root.checkout(self)

        Button:
            text: 'Back'
            size_hint_y: None
            height: 40
            on_press: root.manager.current = 'initial'
'''

class InitialScreen(Screen):
    pass

class LoginChoiceScreen(Screen):
    pass

class RegisterChoiceScreen(Screen):
    pass


class LoginScreen(Screen):
    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.selected_user_type = None  # To track the selected user type

    def on_checkbox_active(self, checkbox, value):
        """Handle checkbox state changes."""
        if value:  # Only when the checkbox is activated (checked)
            if checkbox == self.ids.farmer_checkbox:
                self.selected_user_type = 'farmer'
                print("Farmer selected")
            elif checkbox == self.ids.consumer_checkbox:
                self.selected_user_type = 'consumer'
                print("Consumer selected")

    def login(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if not username or not password:
            self.ids.status_label.text = "Please fill in all fields"
            return

        if self.selected_user_type is None:
            self.ids.status_label.text = "Please select user type"
            return

        response = requests.post('http://localhost:5000/login', json={
            'username': username,
            'password': password,
            'user_type': self.selected_user_type
        })
        response_data = response.json()
        print(f"Response data: {response_data}")

        if response_data.get('message') == 'Login successful':
            self.ids.status_label.text = "Login successful"
            if self.selected_user_type == 'farmer':
                self.manager.current = 'farmer'
            elif self.selected_user_type == 'consumer':
                self.manager.current = 'consumer'
        else:
            self.ids.status_label.text = response_data.get('message', 'Unknown error')

class RegisterChoiceScreen(Screen):
    def __init__(self, **kwargs):
        super(RegisterChoiceScreen, self).__init__(**kwargs)
        self.selected_user_type = None  # To track the selected user type

    def on_checkbox_active(self, checkbox, value):
        """Handle checkbox state changes."""
        if value:  # Only when the checkbox is activated (checked)
            if checkbox == self.ids.farmer_checkbox:
                self.selected_user_type = 'farmer'
                print("Farmer selected")
            elif checkbox == self.ids.consumer_checkbox:
                self.selected_user_type = 'consumer'
                print("Consumer selected")

    def register(self):
        username = self.ids.username.text
        password = self.ids.password.text

        if not username or not password:
            self.ids.status_label.text = "Please fill in all fields"
            return

        if self.selected_user_type is None:
            self.ids.status_label.text = "Please select user type"
            return

        # Debug print
        print(f"Registering user: {username} as {self.selected_user_type}")

        # Example HTTP request to register the user
        response = requests.post('http://localhost:5000/register', json={
            'username': username,
            'password': password,
            'user_type': self.selected_user_type
        })

        response_data = response.json()
        print(f"Response data: {response_data}")

        if response_data.get('message') == 'Registration successful':
            self.ids.status_label.text = "Registration successful"
            if self.selected_user_type == 'farmer':
                self.manager.current = 'login'
            elif self.selected_user_type == 'consumer':
                self.manager.current = 'login'
        else:
            self.ids.status_label.text = response_data.get('message', 'Unknown error')



class FarmerScreen(Screen):

    def __init__(self, **kwargs):
        super(FarmerScreen, self).__init__(**kwargs)
        self.image_path = '/Users/iphone xr pics/image.jpg'

    def open_file_chooser(self, instance):
        """Open file chooser to select an image."""
        filechooser = FileChooserIconView(filters=['*.png', '*.jpg', '*.jpeg'])
        filechooser.bind(on_selection=self.load_image)

        layout = BoxLayout(orientation='vertical')
        layout.add_widget(filechooser)
        self.status_label = Label(text="Select an image", size_hint_y=None, height=50)
        layout.add_widget(self.status_label)

        popup = Popup(title="Select Image", content=layout, size_hint=(0.8, 0.8))
        popup.open()

        self._popup = popup

    def load_image(self, filechooser, selection):
        """Load and display the selected image."""
        if selection:
            self.image_path = selection[0]
            self.ids.image_display.source = self.image_path
            self.ids.image_display.reload()

            self.status_label.text = f"Selected image: {self.image_path}"
            self._popup.dismiss()  # Close the popup after selection
        else:
            self.status_label.text = "No image selected."

    def save_product(self, instance):
        """Save the product details along with the selected image."""
        product_name = self.ids.product_name_input.text
        product_description = self.ids.product_description_input.text
        product_price = self.ids.product_price_input.text

        if self.image_path:
            self.upload_product(product_name, product_description, product_price, self.image_path)
        else:
            self.ids.status_label.text = "Please select an image before saving."

    def upload_product(self, name, description, price, image_path):
        """Upload the product details and image to the server."""
        url = 'http://localhost:5000/upload_product'
        with open(image_path, 'rb') as img_file:
            files = {'file': (image_path, img_file)}
            data = {'name': name, 'description': description, 'price': price}
            response = requests.post(url, files=files, data=data)

            if response.status_code == 200:
                self.ids.status_label.text = "Product added successfully!"
            else:
                self.ids.status_label.text = "Failed to upload the product."


class OrderTrackingScreen(Screen):
    def __init__(self, **kwargs):
        super(OrderTrackingScreen, self).__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')

        self.order_id_input = TextInput(hint_text='Enter Order ID', size_hint_y=None, height=30)
        track_button = Button(text='Track Order', on_press=self.track_order)
        self.status_label = Label(text='Order Status: ')

        layout.add_widget(self.order_id_input)
        layout.add_widget(track_button)
        layout.add_widget(self.status_label)

        self.add_widget(layout)

    def track_order(self, instance):
        order_id = self.order_id_input.text
        status = self.get_order_status(order_id)
        self.status_label.text = f'Order Status: {status}'

    def get_order_status(self, order_id):
        try:
            response = requests.get(f'http://localhost:5000/track_order?order_id={order_id}')
            data = response.json()
            return data['status']
        except requests.RequestException as e:
            return 'Error fetching order status'
class CartScreen(Screen):
    def __init__(self, **kwargs):
        super(CartScreen, self).__init__(**kwargs)
        self.cart_items = []  # List to store cart items
        self.update_cart_view()
        self.update_total()

    def add_to_cart(self, product):
        # Check if product already exists in cart
        for item in self.cart_items:
            if item['name'] == product['name']:
                item['quantity'] += 1
                self.update_cart_view()
                self.update_total()
                return

        # Add new product to cart
        product['quantity'] = 1
        self.cart_items.append(product)
        self.update_cart_view()
        self.update_total()

    def remove_from_cart(self, product_name):
        """Remove a product from the cart."""
        self.cart_items = [item for item in self.cart_items if item['name'] != product_name]
        self.update_cart_view()
        self.update_total()

    def update_cart_view(self):
        """Update the cart view with current items."""
        self.ids.cart_list.clear_widgets()
        for item in self.cart_items:
            item_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
            item_label = Label(text=f"{item['name']} - ${item['price']} x {item['quantity']}")
            remove_button = Button(text='Remove', on_press=lambda btn, name=item['name']: self.remove_from_cart(name))
            add_button = Button(text='+', on_press=lambda btn, item=item: self.change_quantity(item, 1))
            subtract_button = Button(text='-', on_press=lambda btn, item=item: self.change_quantity(item, -1))

            item_layout.add_widget(subtract_button)
            item_layout.add_widget(item_label)
            item_layout.add_widget(add_button)
            item_layout.add_widget(remove_button)

            self.ids.cart_list.add_widget(item_layout)

    def change_quantity(self, item, change):
        """Change the quantity of an item."""
        item['quantity'] += change
        if item['quantity'] <= 0:
            self.remove_from_cart(item['name'])
        else:
            self.update_cart_view()
            self.update_total()

    def update_total(self):
        """Update the total price of the cart."""
        total = sum(item['price'] * item['quantity'] for item in self.cart_items)
        self.ids.total_label.text = f"Total: ${total:.2f}"

    def checkout(self, instance):
        """Proceed to checkout."""
        if not self.cart_items:
            print("Cart is empty. Cannot checkout.")
            return
        
        # Prepare the payload with cart items
        payload = {
            'cart_items': self.cart_items,
            'payment_method': 'credit_card',  # You can modify this as needed
        }

        try:
            # Send the cart items to the server for checkout
            response = requests.post('http://localhost:5000/checkout', json=payload)
            
            if response.status_code == 200:
                print("Checkout successful")
                # Optionally clear the cart after successful checkout
                self.cart_items.clear()
                self.update_cart_view()
                self.update_total()
                print(response.json())  # For debugging, print the response from the server
            else:
                print("Checkout failed")
                print(response.json())  # Print the error message from the server

        except requests.RequestException as e:
            print(f"Error during checkout: {e}")



class ColoredCheckBox(CheckBox):
    background_color = ListProperty([1, 1, 1, 1])  # Default white color

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            self.bg_color = Color()
            self.bg_rect = Rectangle(size=self.size, pos=self.pos)
            self.bind(size=self._update_rect, pos=self._update_rect, background_color=self._update_color)
        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_color(self, instance, value):
        self.bg_color.rgba = value

    def _update_rect(self, instance, value):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

class ConsumerScreen(Screen):
    def __init__(self, **kwargs):
        super(ConsumerScreen, self).__init__(**kwargs)
        self.cart_items = []  # Initialize cart items
        self.current_product = None  # Initialize current product
        self.refresh_products()

    def refresh_products(self, instance=None):
        self.ids.product_list.clear_widgets()  # Clear the product list first
        try:
            response = requests.get('http://localhost:5000/products')
            products = response.json()
            for product in products:
                btn = Button(text=product['name'], size_hint_y=None, height=40)
                btn.bind(on_press=lambda btn, p=product: self.show_product_details(p))
                self.ids.product_list.add_widget(btn)
        except requests.RequestException as e:
            self.ids.product_list.add_widget(Label(text='Failed to fetch products', size_hint_y=None, height=40))

    def show_product_details(self, product):
        self.ids.product_detail_label.text = f"Name: {product['name']}\nDescription: {product['description']}\nPrice: ${product['price']}"
        self.current_product = product
        self.ids.add_to_cart_button.bind(on_press=self.add_to_cart)  # Bind add_to_cart method to button

    def add_to_cart(self, instance):
        # Check if product already exists in cart
        for item in self.cart_items:
            if item['name'] == self.current_product['name']:
                item['quantity'] += 1
                self.update_cart_view()
                self.update_total()
                return

        # Add new product to cart
        self.current_product['quantity'] = 1
        self.cart_items.append(self.current_product)

        # Pass cart items to CartScreen
        cart_screen = self.manager.get_screen('cart')
        cart_screen.cart_items = self.cart_items  # Pass updated cart items to CartScreen
        cart_screen.update_cart_view()
        cart_screen.update_total()

        # Update the status label to indicate success
        self.ids.status_label.text = "Product added successfully!"

    def update_cart_view(self):
        # Update cart view in CartScreen
        cart_screen = self.manager.get_screen('cart')
        cart_screen.update_cart_view()

    def update_total(self):
        # Update total in CartScreen
        cart_screen = self.manager.get_screen('cart')
        cart_screen.update_total()

    def view_cart(self, instance):
        self.manager.current = 'cart'




class MyFarmApp(App):
    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(InitialScreen(name='initial'))
        sm.add_widget(RegisterChoiceScreen(name='register_choice'))
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(RegisterChoiceScreen(name='register'))
        sm.add_widget(FarmerScreen(name='farmer'))
        sm.add_widget(ConsumerScreen(name='consumer'))
        sm.add_widget(OrderTrackingScreen(name='order_tracking'))
        sm.add_widget(CartScreen(name='cart'))
        return sm


if __name__ == '__main__':
    MyFarmApp().run()
