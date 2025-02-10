import streamlit as st
import stripe

# Stripe API Keys (Replace with your own)
stripe.api_key = "sk_test_51QqxwJKy4jxgQ38B4c0oCQbIVJDjUNRAyAlO69tc6UoqXB4j2gri4EFUnG9ydrYBzc4V4te26iXeATFi0a94QKif00WneKObON"  # Replace with your actual Stripe Secret Key
STRIPE_PUBLIC_KEY = "pk_test_51QqxwJKy4jxgQ38B5a1nDQQiDV3EaFMUm9QN1h82maOMgwjmf2SteeKs8qqpepYTDPdxjT0l9Iun1fHKUKqM1Wr000EJDJXBMi"  # Replace with your actual Stripe Public Key

# Default Tourism Countries (With Placeholder)
tourism_countries = ["Select your destination"] + [
    "France", "Spain", "United States", "Italy", "Turkey", "Morocco", "Thailand", "Japan",
    "Germany", "Greece", "China", "India", "Indonesia", "United Kingdom", "Mexico", "Australia"
]

# Default Interests List (With Placeholder)
interests_list = ["Select your interest"] + [
    "Cooking with Locals", "Hidden Nature Trails", "Cultural Immersion",
    "Adventure Sports", "Historical Tours", "Street Food & Markets", "Art & Handicrafts",
    "Wildlife Safaris", "Music & Dance Workshops"
]

# Available Hosts and Services (for each country)
hosts_data = {
    "France": [
        {"name": "Pierre", "service": "Parisian Bakery & Pastry Workshop", "price": 55},
        {"name": "Camille", "service": "Louvre After-Hours Art Tour", "price": 80}
    ],
    "Spain": [
        {"name": "Alejandro", "service": "Authentic Paella Cooking Class", "price": 50},
        {"name": "Sofia", "service": "Flamenco Dance & Guitar Workshop", "price": 60}
    ],
    "United States": [
        {"name": "Jake", "service": "New York Street Food & Hidden Gems Tour", "price": 75},
        {"name": "Linda", "service": "Hollywood Film Industry Behind-the-Scenes", "price": 90}
    ],
    "Italy": [
        {"name": "Luigi", "service": "Pizza Making with a Local Chef", "price": 65},
        {"name": "Giulia", "service": "Vineyard Tour & Wine Tasting", "price": 80}
    ],
    "Turkey": [
        {"name": "Mehmet", "service": "Turkish Coffee & Baklava Tasting", "price": 40},
        {"name": "Aylin", "service": "Hot Air Balloon Ride in Cappadocia", "price": 120}
    ],
    "Morocco": [
        {"name": "Ahmed", "service": "Cooking with Locals", "price": 50},
        {"name": "Fatima", "service": "Marrakech Hidden Market Tour", "price": 40},
        {"name": "Fatima", "service": "Traditional Moroccan Cooking Class", "price": 40}
    ],
    "Thailand": [
        {"name": "Niran", "service": "Bangkok Floating Market Experience", "price": 55},
        {"name": "Anong", "service": "Thai Massage & Wellness Retreat", "price": 70}
    ],
    "Japan": [
        {"name": "Hiroshi", "service": "Samurai Sword Experience", "price": 75},
        {"name": "Naoko", "service": "Kyoto Tea Ceremony", "price": 60}
    ],
    "Mexico": [
        {"name": "Carlos", "service": "Authentic Taco & Tequila Tasting", "price": 45},
        {"name": "Isabella", "service": "Chichen Itza Mayan Civilization Tour", "price": 75}
    ],
    "Australia": [
        {"name": "Steve", "service": "Sydney Harbour Kayaking Adventure", "price": 85},
        {"name": "Jessica", "service": "Great Barrier Reef Diving Experience", "price": 120}
    ]
}

# Function to Get Available Hosts
def get_available_hosts(destination, interest):
    """
    Retrieves hosts offering experiences based on user selection.
    """
    if destination == "Select your destination" or interest == "Select your interest":
        return "Please select a valid destination and interest."
    
    hosts = hosts_data.get(destination, [])
    matching_hosts = [h for h in hosts if interest.lower() in h["service"].lower()]
    
    return matching_hosts if matching_hosts else "No hosts found for this interest."

# Function to calculate total price with commission
def calculate_total_price(base_price):
    commission_rate = 0.05  # 5% commission
    commission_fee = base_price * commission_rate
    total_price = base_price + commission_fee
    return total_price, commission_fee

# Function to create Stripe Checkout Session
def create_checkout_session(host_name, service_name, total_price):
    """
    Creates a Stripe checkout session and returns the checkout URL.
    """
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': f"{service_name} ",
                },
                'unit_amount': int(total_price * 100),  # Stripe expects amount in cents
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url="https://your-app-url.com/success",
        cancel_url="https://your-app-url.com/cancel",
    )
    return session.url

# Streamlit UI
st.set_page_config(page_title="Culturo - Authentic Travel", layout="wide")

# Display the logo
st.image("logo.jpg", width=250)  # Adjust width as needed

# Header with Styling
st.markdown(
    "<h1 style='text-align: center; color: #2E86C1;'>🌍 Welcome to Culturo </h1>", 
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; color: #34495E;'>Explore culture like never before.</h3>", 
    unsafe_allow_html=True
)

# User Selection
st.markdown("## 🌍 Find Your Authentic Experience")
destination = st.selectbox("Select a destination:", tourism_countries, index=0)  # Default Placeholder
interest = st.selectbox("Choose an experience:", interests_list, index=0)  # Default Placeholder

if st.button("Find Experiences"):
    if destination != "Select your destination" and interest != "Select your interest":
        with st.spinner("Finding experiences..."):
            available_hosts = get_available_hosts(destination, interest)

            st.markdown("### 🏡 Available Hosts & Services")
            if isinstance(available_hosts, list):
                for host in available_hosts:
                    base_price = host["price"]
                    total_price, commission_fee = calculate_total_price(base_price)

                    st.write(f"👤 *{host['name']}* - {host['service']}")
                    st.write(f"💰 Base Price: ${base_price}")
                    st.write(f"🔹 Platform Fee (5%): ${commission_fee:.2f}")
                    st.write(f"💳 *Total Price: ${total_price:.2f}*")

                    # Pay Button with Stripe Integration
                    checkout_url = create_checkout_session(host["name"], host["service"], total_price)
                    st.markdown(f"[🛒 Pay Now - {host['name']}]({checkout_url})", unsafe_allow_html=True)
            else:
                st.warning(available_hosts)
    else:
        st.warning("Please select both a destination and an experience.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.text("© 2025 Culturo – Explore culture like never before.")