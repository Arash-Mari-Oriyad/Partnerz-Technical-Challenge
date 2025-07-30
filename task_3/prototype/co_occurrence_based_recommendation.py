from utils import (
    generate_products,
    generate_transactions,
    create_co_occurrence_matrix,
    get_recommendations,
)


all_products = generate_products()

transaction_data = generate_transactions(all_products=all_products)


print(f"--- Synthetic Transaction Data ({len(transaction_data)} transactions) ---")
for i, transaction in enumerate(
    transaction_data[:10]
):  # Print only first 10 for brevity
    print(f"Transaction {i+1}: {transaction}")
if len(transaction_data) > 10:
    print(f"... {len(transaction_data) - 10} more transactions ...")
print("\n" + "=" * 40 + "\n")


co_occurrence_matrix, item_confidence_scores = create_co_occurrence_matrix(
    transaction_data=transaction_data
)

print("--- Generating Recommendations with Expanded Data ---")

# Scenario 1: User views 'Laptop_XPS_13'
viewed_product_1 = "Laptop_XPS_13"
recs_1_counts = get_recommendations(
    viewed_product_1, num_recommendations=5, metric_matrix=co_occurrence_matrix
)
recs_1_confidence = get_recommendations(
    viewed_product_1, num_recommendations=5, metric_matrix=item_confidence_scores
)
print(f"\nIf customer views '{viewed_product_1}':")
print(f"  Recommended (by raw co-occurrence count): {recs_1_counts}")
print(f"  Recommended (by confidence score): {recs_1_confidence}")

# Scenario 2: User views 'Instant_Pot_Duo'
viewed_product_2 = "Instant_Pot_Duo"
recs_2_counts = get_recommendations(
    viewed_product_2, num_recommendations=5, metric_matrix=co_occurrence_matrix
)
recs_2_confidence = get_recommendations(
    viewed_product_2, num_recommendations=5, metric_matrix=item_confidence_scores
)
print(f"\nIf customer views '{viewed_product_2}':")
print(f"  Recommended (by raw co-occurrence count): {recs_2_counts}")
print(f"  Recommended (by confidence score): {recs_2_confidence}")

# Scenario 3: User views 'Mens_T-Shirt_Cotton'
viewed_product_3 = "Mens_T-Shirt_Cotton"
recs_3_counts = get_recommendations(
    viewed_product_3, num_recommendations=5, metric_matrix=co_occurrence_matrix
)
recs_3_confidence = get_recommendations(
    viewed_product_3, num_recommendations=5, metric_matrix=item_confidence_scores
)
print(f"\nIf customer views '{viewed_product_3}':")
print(f"  Recommended (by raw co-occurrence count): {recs_3_counts}")
print(f"  Recommended (by confidence score): {recs_3_confidence}")
