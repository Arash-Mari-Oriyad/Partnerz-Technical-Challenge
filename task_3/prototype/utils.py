import random
from collections import defaultdict


def generate_products():
    electronics_laptops = [
        "Laptop_XPS_13",
        "MacBook_Air_M3",
        "HP_Spectre_x360",
        "Lenovo_ThinkPad_T14",
    ]
    electronics_peripherals = [
        "Logitech_MX_Master_3",
        "Apple_Magic_Keyboard",
        "Dell_UltraSharp_Monitor",
        "Sony_WH-1000XM5_Headphones",
        "Rode_NT-USB_Mic",
        "Logitech_C920_Webcam",
    ]
    electronics_storage = ["Samsung_T7_SSD", "Crucial_X8_SSD", "WD_My_Passport_HDD"]
    electronics_accessories = [
        "USB-C_Hub",
        "HDMI_Cable_2m",
        "Laptop_Sleeve_13in",
        "Monitor_Stand",
    ]
    home_kitchen_appliances = [
        "Instant_Pot_Duo",
        "Ninja_Foodi_Blender",
        "Keurig_K-Elite",
        "Dyson_V11_Vacuum",
    ]
    home_kitchen_cookware = [
        "Cast_Iron_Skillet",
        "Non-Stick_Pan_Set",
        "Silicone_Spatula_Set",
    ]
    home_kitchen_decor = ["Smart_LED_Bulb", "Aroma_Diffuser", "Throw_Pillow_Set"]
    apparel_mens = ["Mens_T-Shirt_Cotton", "Mens_Jeans_SlimFit", "Mens_Hoodie_Fleece"]
    apparel_womens = [
        "Womens_Blouse_Silk",
        "Womens_Leggings_Yoga",
        "Womens_Dress_Summer",
    ]
    apparel_accessories = ["Leather_Wallet", "Sports_Socks_3pk", "Baseball_Cap"]
    all_products = (
        electronics_laptops
        + electronics_peripherals
        + electronics_storage
        + electronics_accessories
        + home_kitchen_appliances
        + home_kitchen_cookware
        + home_kitchen_decor
        + apparel_mens
        + apparel_womens
        + apparel_accessories
    )
    return all_products


def generate_transactions(all_products):
    transaction_data = [
        # Laptop & Peripherals bundles
        [
            "Laptop_XPS_13",
            "Logitech_MX_Master_3",
            "Dell_UltraSharp_Monitor",
            "USB-C_Hub",
        ],
        [
            "MacBook_Air_M3",
            "Apple_Magic_Keyboard",
            "Logitech_C920_Webcam",
            "Laptop_Sleeve_13in",
        ],
        ["HP_Spectre_x360", "Sony_WH-1000XM5_Headphones", "Samsung_T7_SSD"],
        ["Lenovo_ThinkPad_T14", "Logitech_MX_Master_3", "Rode_NT-USB_Mic"],
        ["Laptop_XPS_13", "Samsung_T7_SSD", "USB-C_Hub"],
        ["MacBook_Air_M3", "Laptop_Sleeve_13in"],
        ["Dell_UltraSharp_Monitor", "HDMI_Cable_2m", "Monitor_Stand"],
        ["Logitech_MX_Master_3", "Logitech_C920_Webcam"],
        ["Sony_WH-1000XM5_Headphones", "Rode_NT-USB_Mic"],
        # Home & Kitchen bundles
        ["Instant_Pot_Duo", "Non-Stick_Pan_Set", "Silicone_Spatula_Set"],
        ["Ninja_Foodi_Blender", "Smart_LED_Bulb"],
        ["Keurig_K-Elite", "Aroma_Diffuser"],
        ["Dyson_V11_Vacuum", "Smart_LED_Bulb", "Throw_Pillow_Set"],
        ["Instant_Pot_Duo", "Cast_Iron_Skillet"],
        ["Non-Stick_Pan_Set", "Silicone_Spatula_Set"],
        ["Keurig_K-Elite", "Throw_Pillow_Set"],
        # Apparel bundles
        ["Mens_T-Shirt_Cotton", "Mens_Jeans_SlimFit", "Leather_Wallet"],
        ["Womens_Blouse_Silk", "Womens_Leggings_Yoga"],
        ["Mens_Hoodie_Fleece", "Baseball_Cap", "Sports_Socks_3pk"],
        ["Womens_Dress_Summer", "Leather_Wallet"],
        ["Mens_Jeans_SlimFit", "Sports_Socks_3pk"],
        ["Womens_Leggings_Yoga", "Womens_Blouse_Silk"],
        # Mixed bundles (less common but realistic)
        ["Laptop_XPS_13", "Instant_Pot_Duo"],
        ["Dyson_V11_Vacuum", "Apple_Magic_Keyboard"],
        ["Mens_T-Shirt_Cotton", "Smart_LED_Bulb"],
        ["Keurig_K-Elite", "Logitech_MX_Master_3"],
        ["Womens_Dress_Summer", "Samsung_T7_SSD"],
        ["Monitor_Stand", "Aroma_Diffuser"],
        ["Cast_Iron_Skillet", "HDMI_Cable_2m"],
        ["Baseball_Cap", "Crucial_X8_SSD"],
        ["Non-Stick_Pan_Set", "Laptop_Sleeve_13in"],
        ["Rode_NT-USB_Mic", "Throw_Pillow_Set"],
        ["Womens_Leggings_Yoga", "USB-C_Hub"],
        ["Mens_Hoodie_Fleece", "WD_My_Passport_HDD"],
        ["Instant_Pot_Duo", "Logitech_C920_Webcam"],
        ["MacBook_Air_M3", "Non-Stick_Pan_Set"],
        ["HP_Spectre_x360", "Womens_Blouse_Silk"],
        ["Lenovo_ThinkPad_T14", "Mens_T-Shirt_Cotton"],
        ["Dell_UltraSharp_Monitor", "Dyson_V11_Vacuum"],
        ["Sony_WH-1000XM5_Headphones", "Keurig_K-Elite"],
        ["Samsung_T7_SSD", "Cast_Iron_Skillet"],
        ["Crucial_X8_SSD", "Smart_LED_Bulb"],
        ["WD_My_Passport_HDD", "Aroma_Diffuser"],
        ["USB-C_Hub", "Throw_Pillow_Set"],
        ["HDMI_Cable_2m", "Leather_Wallet"],
        ["Laptop_Sleeve_13in", "Sports_Socks_3pk"],
        ["Monitor_Stand", "Baseball_Cap"],
    ]
    # Add some more random transactions to increase data volume and noise
    num_additional_transactions = 50
    for _ in range(num_additional_transactions):
        num_items = random.randint(1, 5)
        transaction = random.sample(all_products, min(num_items, len(all_products)))
        transaction_data.append(transaction)
    return transaction_data


def create_co_occurrence_matrix(transaction_data):
    # Initialize a co-occurrence matrix
    co_occurrence_matrix = defaultdict(lambda: defaultdict(int))
    item_counts = defaultdict(int)

    # Populate the co-occurrence matrix and item counts
    for transaction in transaction_data:
        unique_transaction_items = list(set(transaction))
        for item in unique_transaction_items:
            item_counts[item] += 1
            for item2 in unique_transaction_items:
                if item != item2:  # Don't count an item co-occurring with itself
                    co_occurrence_matrix[item][item2] += 1

    # --- Calculate Confidence Score ---
    # Confidence(A -> B) = P(B|A) = Count(A & B) / Count(A)
    # This measures how likely it is that B is bought if A is bought.
    item_confidence_scores = defaultdict(lambda: defaultdict(float))
    for item1, co_occurrences in co_occurrence_matrix.items():
        for item2, count in co_occurrences.items():
            if item_counts[item1] > 0:  # Avoid division by zero
                confidence = count / item_counts[item1]
                item_confidence_scores[item1][item2] = confidence
    return co_occurrence_matrix, item_confidence_scores


def get_recommendations(product_id, num_recommendations=5, metric_matrix=None):
    """
    Generates 'Customers also bought' recommendations for a given product ID.

    Args:
        product_id (str): The ID of the product currently being viewed.
        num_recommendations (int): The maximum number of recommendations to return.
        metric_matrix (dict): The matrix (e.g., co_occurrence_matrix or item_confidence_scores)
        to use for ranking recommendations. Defaults to co-occurrence counts.

    Returns:
        list: A list of recommended product IDs, sorted by relevance.
    """
    if product_id not in metric_matrix:
        print(
            f"No recommendations found for '{product_id}'. It might be a new item or have insufficient data."
        )
        return []
    recommendation_scores = metric_matrix[product_id]
    sorted_recommendations = sorted(
        recommendation_scores.items(), key=lambda item: item[1], reverse=True
    )
    recommended_product_ids = [
        item[0] for item in sorted_recommendations[:num_recommendations]
    ]
    return recommended_product_ids
