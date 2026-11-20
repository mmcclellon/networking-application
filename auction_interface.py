def show_menu():
    print("\n========== SOLD! AUCTION HOUSE ==========")
    print("1. View available auctions")
    print("2. Place a bid")
    print("3. Refresh auctions")
    print("4. Exit")
    print("=========================================")

# Sample auction data for testing
auctions = [
    {
        "id": 1,
        "item": "Gaming Laptop",
        "current_bid": 450.00,
        "highest_bidder": "Alice",
        "status": "Active"
    },
    {
        "id": 2,
        "item": "Wireless Headphones",
        "current_bid": 75.00,
        "highest_bidder": "John",
        "status": "Active"
    },
    {
        "id": 3,
        "item": "Smart Watch",
        "current_bid": 120.00,
        "highest_bidder": "Sarah",
        "status": "Active"
    }
]


def view_auctions():
    print("\n========== AVAILABLE AUCTIONS ==========")

    if not auctions:
        print("There are currently no available auctions.")
        return

    for auction in auctions:
        print("----------------------------------------")
        print("Auction ID:", auction["id"])
        print("Item:", auction["item"])
        print("Current bid: $", auction["current_bid"])
        print("Highest bidder:", auction["highest_bidder"])
        print("Status:", auction["status"])

    print("----------------------------------------")


def place_bid():
    print("\n========== PLACE A BID ==========")

    try:
        auction_id = int(input("Enter auction ID: "))

        # Find the selected auction
        selected_auction = None

        for auction in auctions:
            if auction["id"] == auction_id:
                selected_auction = auction
                break

        if selected_auction is None:
            print("Auction not found.")
            return

        # Check whether the auction is active
        if selected_auction["status"] != "Active":
            print("Sorry, this auction has ended.")
            return

        print("\nItem:", selected_auction["item"])
        print("Current bid: $", selected_auction["current_bid"])
        print("Highest bidder:", selected_auction["highest_bidder"])

        # Ask user for their bid
        bid_amount = float(input("\nEnter your bid amount: $"))

        # Validate bid
        if bid_amount <= selected_auction["current_bid"]:
            print("Bid rejected! Your bid must be higher than the current bid.")
            return

        if bid_amount <= 0:
            print("Invalid bid amount.")
            return

        # Update auction information
        selected_auction["current_bid"] = bid_amount
        selected_auction["highest_bidder"] = "You"

        print("\nCongratulations! Your bid was accepted.")
        print("New highest bid: $", selected_auction["current_bid"])

    except ValueError:
        print("Invalid input. Please enter a valid number.")


def refresh_auctions():
    print("\nRefreshing auction listings...")

    # Redisplay the current auction data
    view_auctions()


def main():
    while True:
        show_menu()

        choice = input("Please select an option: ").strip()

        if choice == "1":
            view_auctions()

        elif choice == "2":
            place_bid()

        elif choice == "3":
            refresh_auctions()

        elif choice == "4":
            print("\nThank you for using SOLD!")
            break

        else:
            print("\nInvalid choice. Please select 1-4.")


if __name__ == "__main__":
    main()