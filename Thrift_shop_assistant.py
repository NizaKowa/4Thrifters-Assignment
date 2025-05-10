#!/usr/bin/env python3
"""
Thrift Shop Assistant - A CLI tool for recommending thrifted clothing items.
This program helps users find clothing items that match their preferences through
an interactive question-and-answer process with fuzzy matching capabilities.
"""

import json
import difflib
import os
import random
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional, Set, Tuple


@dataclass
class ClothingItem:
    """Class representing a thrifted clothing item with various attributes."""
    id: str
    name: str
    category: str
    color: str
    style: str
    season: List[str]
    material: str
    occasion: List[str]
    gender: str
    size: str
    condition: str
    price: float
    description: str = ""
    
    def match_score(self, preferences: Dict[str, Any]) -> float:
        """
        Calculate how well this item matches the given preferences.
        Returns a score between 0.0 and 1.0, where 1.0 is a perfect match.
        """
        score = 0.0
        total_weights = 0.0
        
        # Define weights for different attributes (can be adjusted)
        weights = {
            "category": 1.5,
            "color": 1.0,
            "style": 1.2,
            "season": 0.8,
            "material": 0.7,
            "occasion": 1.3,
            "gender": 1.4,
            "size": 1.0,
            "condition": 0.6,
            "price_range": 0.9
        }
        
        for attr, pref_value in preferences.items():
            if not pref_value:  # Skip if no preference specified
                continue
                
            if attr == "price_range" and preferences.get("price_range"):
                min_price, max_price = preferences["price_range"]
                if min_price <= self.price <= max_price:
                    score += weights[attr]
                total_weights += weights[attr]
                continue
            
            # Handle list attributes (season, occasion)
            if attr in ["season", "occasion"]:
                item_value = getattr(self, attr)
                if isinstance(pref_value, list):
                    # Check if any preferred value is in the item's values
                    matches = len(set(pref_value).intersection(set(item_value)))
                    if matches > 0:
                        score += weights[attr] * (matches / len(pref_value))
                else:
                    # Single value preference
                    if pref_value in item_value:
                        score += weights[attr]
                total_weights += weights[attr]
                continue
            
            # For text attributes, use fuzzy matching
            item_value = getattr(self, attr, "")
            if not item_value:
                continue
                
            # Use fuzzy matching for text comparison
            similarity = difflib.SequenceMatcher(None, 
                                              str(pref_value).lower(), 
                                              str(item_value).lower()).ratio()
            
            # Only count as a match if similarity is above threshold
            if similarity > 0.7:
                score += weights.get(attr, 1.0) * similarity
                
            total_weights += weights.get(attr, 1.0)
        
        # Normalize score
        return score / total_weights if total_weights > 0 else 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert the item to a dictionary."""
        return asdict(self)
        
    def display(self) -> None:
        """Display the item in a user-friendly format."""
        print(f"\n{'=' * 60}")
        print(f"🏷️  {self.name.upper()} (ID: {self.id})")
        print(f"{'=' * 60}")
        print(f"📋 Category: {self.category}")
        print(f"🎨 Color: {self.color}")
        print(f"👗 Style: {self.style}")
        print(f"🌡️  Season: {', '.join(self.season)}")
        print(f"🧵 Material: {self.material}")
        print(f"🎭 Occasion: {', '.join(self.occasion)}")
        print(f"👤 Gender: {self.gender}")
        print(f"📏 Size: {self.size}")
        print(f"✨ Condition: {self.condition}")
        print(f"💰 Price: ${self.price:.2f}")
        
        if self.description:
            print(f"\n📝 Description: {self.description}")
        
        print(f"{'=' * 60}")


class ThriftShopAssistant:
    """
    The main class for the Thrift Shop Assistant application.
    Handles loading inventory, user interactions, and recommendations.
    """
    
    def __init__(self, inventory_file: str = None):
        """Initialize the assistant with inventory data."""
        self.items: List[ClothingItem] = []
        
        # Try to load from file if provided, otherwise use default data
        if inventory_file and os.path.exists(inventory_file):
            self._load_inventory(inventory_file)
        else:
            self._create_default_inventory()
    
    def _load_inventory(self, inventory_file: str) -> None:
        """Load inventory from a JSON file."""
        try:
            with open(inventory_file, 'r') as file:
                items_data = json.load(file)
                for item_data in items_data:
                    self.items.append(ClothingItem(**item_data))
            print(f"Loaded {len(self.items)} items from {inventory_file}")
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error loading inventory: {e}")
            print("Using default inventory instead.")
            self._create_default_inventory()
    
    def _create_default_inventory(self) -> None:
        """Create a default inventory with sample items."""
        self.items = [
            ClothingItem(
                id="TS001",
                name="Vintage Denim Jacket",
                category="Outerwear",
                color="Blue",
                style="Vintage",
                season=["Spring", "Fall"],
                material="Denim",
                occasion=["Casual", "Streetwear"],
                gender="Unisex",
                size="M",
                condition="Good",
                price=24.99,
                description="Classic 90s denim jacket with minor distressing for that authentic look."
            ),
            ClothingItem(
                id="TS002",
                name="Floral Summer Dress",
                category="Dress",
                color="Multicolor",
                style="Bohemian",
                season=["Summer", "Spring"],
                material="Cotton",
                occasion=["Casual", "Daytime"],
                gender="Women",
                size="S",
                condition="Excellent",
                price=18.50,
                description="Light and airy sundress with a delicate floral pattern."
            ),
            ClothingItem(
                id="TS003",
                name="Wool Peacoat",
                category="Outerwear",
                color="Navy",
                style="Classic",
                season=["Winter", "Fall"],
                material="Wool",
                occasion=["Formal", "Work"],
                gender="Men",
                size="L",
                condition="Very Good",
                price=35.00,
                description="Warm wool peacoat perfect for cold weather, with original buttons."
            ),
            ClothingItem(
                id="TS004",
                name="Graphic Band T-Shirt",
                category="Top",
                color="Black",
                style="Rock",
                season=["All"],
                material="Cotton",
                occasion=["Casual", "Concert"],
                gender="Unisex",
                size="M",
                condition="Good",
                price=12.99,
                description="Faded vintage rock band t-shirt with original tour dates."
            ),
            ClothingItem(
                id="TS005",
                name="High-Waisted Jeans",
                category="Bottoms",
                color="Light Blue",
                style="Retro",
                season=["All"],
                material="Denim",
                occasion=["Casual", "Everyday"],
                gender="Women",
                size="28",
                condition="Excellent",
                price=22.50,
                description="Classic high-waisted mom jeans with a relaxed fit."
            ),
            ClothingItem(
                id="TS006",
                name="Leather Biker Jacket",
                category="Outerwear",
                color="Black",
                style="Edgy",
                season=["Fall", "Winter"],
                material="Leather",
                occasion=["Night Out", "Casual"],
                gender="Unisex",
                size="M",
                condition="Very Good",
                price=45.00,
                description="Genuine leather biker jacket with silver hardware and minimal wear."
            ),
            ClothingItem(
                id="TS007",
                name="Plaid Flannel Shirt",
                category="Top",
                color="Red",
                style="Grunge",
                season=["Fall", "Winter"],
                material="Cotton",
                occasion=["Casual", "Outdoor"],
                gender="Unisex",
                size="L",
                condition="Good",
                price=14.50,
                description="Soft and worn-in flannel with a classic red plaid pattern."
            ),
            ClothingItem(
                id="TS008",
                name="Knit Sweater",
                category="Top",
                color="Cream",
                style="Cozy",
                season=["Winter", "Fall"],
                material="Wool Blend",
                occasion=["Casual", "Holiday"],
                gender="Unisex",
                size="XL",
                condition="Very Good",
                price=19.99,
                description="Chunky knit sweater perfect for staying warm on cold days."
            ),
            ClothingItem(
                id="TS009",
                name="Silk Blouse",
                category="Top",
                color="Emerald",
                style="Elegant",
                season=["Spring", "Summer", "Fall"],
                material="Silk",
                occasion=["Work", "Formal"],
                gender="Women",
                size="M",
                condition="Excellent",
                price=25.00,
                description="Luxurious silk blouse with subtle button details and a flowing fit."
            ),
            ClothingItem(
                id="TS010",
                name="Cargo Shorts",
                category="Bottoms",
                color="Khaki",
                style="Casual",
                season=["Summer"],
                material="Cotton",
                occasion=["Casual", "Outdoor"],
                gender="Men",
                size="32",
                condition="Good",
                price=16.50,
                description="Durable cargo shorts with multiple pockets, perfect for summer adventures."
            ),
            ClothingItem(
                id="TS011",
                name="Velvet Evening Gown",
                category="Dress",
                color="Burgundy",
                style="Formal",
                season=["Winter", "Fall"],
                material="Velvet",
                occasion=["Formal", "Party"],
                gender="Women",
                size="M",
                condition="Excellent",
                price=42.00,
                description="Stunning floor-length velvet gown perfect for special occasions."
            ),
            ClothingItem(
                id="TS012",
                name="Corduroy Button-Down Shirt",
                category="Top",
                color="Mustard",
                style="Vintage",
                season=["Fall", "Winter"],
                material="Corduroy",
                occasion=["Casual", "Work"],
                gender="Unisex",
                size="S",
                condition="Very Good",
                price=18.75,
                description="Soft corduroy shirt with a retro 70s feel in a warm mustard tone."
            ),
            ClothingItem(
                id="TS013",
                name="Leather Cowboy Boots",
                category="Footwear",
                color="Brown",
                style="Western",
                season=["All"],
                material="Leather",
                occasion=["Casual", "Festival"],
                gender="Unisex",
                size="9",
                condition="Good",
                price=29.99,
                description="Authentic vintage cowboy boots with natural wear that adds character."
            ),
            ClothingItem(
                id="TS014",
                name="Linen Blazer",
                category="Outerwear",
                color="Beige",
                style="Smart Casual",
                season=["Spring", "Summer"],
                material="Linen",
                occasion=["Work", "Semi-formal"],
                gender="Men",
                size="M",
                condition="Very Good",
                price=32.00,
                description="Lightweight linen blazer, perfect for warm weather formal occasions."
            ),
            ClothingItem(
                id="TS015",
                name="Beaded Clutch Purse",
                category="Accessory",
                color="Silver",
                style="Vintage Glamour",
                season=["All"],
                material="Beads & Satin",
                occasion=["Formal", "Party"],
                gender="Women",
                size="One Size",
                condition="Excellent",
                price=23.50,
                description="Elegant vintage clutch with intricate beadwork, perfect for special occasions."
            )
        ]
        print(f"Created default inventory with {len(self.items)} items")
    
    def save_inventory(self, filename: str) -> None:
        """Save the current inventory to a JSON file."""
        items_data = [item.to_dict() for item in self.items]
        try:
            with open(filename, 'w') as file:
                json.dump(items_data, file, indent=2)
            print(f"Inventory saved to {filename}")
        except Exception as e:
            print(f"Error saving inventory: {e}")
    
    def _fuzzy_match(self, user_input: str, options: List[str], threshold: float = 0.6) -> Optional[str]:
        """
        Match user input against a list of options using fuzzy matching.
        Returns the best match if it's above the threshold, otherwise None.
        """
        if not user_input or not options:
            return None
            
        # Clean and lowercase the input
        user_input = user_input.strip().lower()
        
        # Check for exact matches first
        for option in options:
            if option.lower() == user_input:
                return option
        
        # Then do fuzzy matching
        matches = []
        for option in options:
            ratio = difflib.SequenceMatcher(None, user_input, option.lower()).ratio()
            matches.append((option, ratio))
        
        # Sort by match ratio (highest first)
        matches.sort(key=lambda x: x[1], reverse=True)
        
        # Return the best match if it's above the threshold
        if matches and matches[0][1] >= threshold:
            return matches[0][0]
            
        return None
    
    def _get_unique_values(self, attribute: str) -> List[str]:
        """Get a list of unique values for a given attribute across all items."""
        if attribute in ["season", "occasion"]:
            # Handle list attributes
            values = set()
            for item in self.items:
                attr_value = getattr(item, attribute)
                if isinstance(attr_value, list):
                    values.update(attr_value)
                else:
                    values.add(attr_value)
            return sorted(list(values))
        else:
            # Handle scalar attributes
            return sorted(list(set(getattr(item, attribute) for item in self.items)))
    
    def _ask_question(self, prompt: str, options: List[str] = None, 
                     allow_multiple: bool = False, allow_skip: bool = True) -> Any:
        """
        Ask the user a question and return their response.
        If options are provided, validate against them with fuzzy matching.
        """
        while True:
            if options:
                option_str = ", ".join(options)
                skip_str = " (or press Enter to skip)" if allow_skip else ""
                multi_str = " (separate multiple choices with commas)" if allow_multiple else ""
                print(f"\n{prompt} [{option_str}]{multi_str}{skip_str}: ", end="")
            else:
                skip_str = " (or press Enter to skip)" if allow_skip else ""
                print(f"\n{prompt}{skip_str}: ", end="")
            
            response = input().strip()
            
            # Handle skip
            if not response and allow_skip:
                return None if not allow_multiple else []
            
            if options:
                if allow_multiple:
                    # Handle multiple selections
                    selections = [r.strip() for r in response.split(",")]
                    valid_selections = []
                    
                    for selection in selections:
                        match = self._fuzzy_match(selection, options)
                        if match:
                            valid_selections.append(match)
                        else:
                            print(f"Sorry, '{selection}' isn't a valid option.")
                    
                    if valid_selections:
                        return valid_selections
                    print("Please try again with valid options.")
                else:
                    # Handle single selection
                    match = self._fuzzy_match(response, options)
                    if match:
                        return match
                    print(f"Sorry, '{response}' isn't a valid option. Please try again.")
            else:
                # No validation needed
                return response
    
    def _ask_price_range(self) -> Optional[Tuple[float, float]]:
        """Ask the user for their budget range."""
        print("\nWhat's your budget range?")
        
        try:
            min_input = input("Minimum price ($ or press Enter to skip): $").strip()
            if not min_input:
                return None
            
            min_price = float(min_input)
            max_input = input("Maximum price ($ or press Enter for no max): $").strip()
            max_price = float(max_input) if max_input else float('inf')
            
            if min_price < 0 or (max_price != float('inf') and max_price < min_price):
                print("Invalid price range. Using no price filter.")
                return None
                
            return (min_price, max_price)
        except ValueError:
            print("Invalid price format. Using no price filter.")
            return None
    
    def gather_preferences(self) -> Dict[str, Any]:
        """
        Interactive function to gather user preferences through a series of questions.
        Returns a dictionary of preferences.
        """
        preferences = {}
        print("\n🛍️ Welcome to the Thrift Shop Assistant! 🛍️")
        print("I'll help you find the perfect thrifted item for your style.")
        print("Let me ask you a few questions to understand what you're looking for.")
        
        # Get item category preference
        categories = self._get_unique_values("category")
        preferences["category"] = self._ask_question(
            "What type of clothing are you looking for?", 
            categories
        )
        
        # Get occasion
        occasions = self._get_unique_values("occasion")
        preferences["occasion"] = self._ask_question(
            "What occasion are you shopping for?", 
            occasions, 
            allow_multiple=True
        )
        
        # Get season preference
        seasons = self._get_unique_values("season")
        preferences["season"] = self._ask_question(
            "Which season are you shopping for?", 
            seasons, 
            allow_multiple=True
        )
        
        # Get color preference
        colors = self._get_unique_values("color")
        preferences["color"] = self._ask_question(
            "Do you have a color preference?", 
            colors
        )
        
        # Get style preference
        styles = self._get_unique_values("style")
        preferences["style"] = self._ask_question(
            "What style are you interested in?", 
            styles
        )
        
        # Get gender preference
        genders = self._get_unique_values("gender")
        preferences["gender"] = self._ask_question(
            "Gender preference?", 
            genders
        )
        
        # Get size preference
        sizes = self._get_unique_values("size")
        preferences["size"] = self._ask_question(
            "What size are you looking for?", 
            sizes
        )
        
        # Get material preference
        materials = self._get_unique_values("material")
        preferences["material"] = self._ask_question(
            "Do you have a preferred material?", 
            materials
        )
        
        # Get condition preference
        conditions = self._get_unique_values("condition")
        preferences["condition"] = self._ask_question(
            "What's your minimum acceptable condition?", 
            conditions
        )
        
        # Get price range
        preferences["price_range"] = self._ask_price_range()
        
        return preferences
    
    def recommend_items(self, preferences: Dict[str, Any], top_n: int = 3) -> List[ClothingItem]:
        """
        Recommend items based on user preferences.
        Returns up to top_n items sorted by match score.
        """
        if not preferences:
            return []
            
        # Calculate match scores for all items
        scored_items = []
        for item in self.items:
            score = item.match_score(preferences)
            scored_items.append((item, score))
        
        # Sort by score (highest first)
        scored_items.sort(key=lambda x: x[1], reverse=True)
        
        # Filter out items with very low scores (less than 50% match)
        good_matches = [(item, score) for item, score in scored_items if score > 0.5]
        
        if not good_matches:
            return []
            
        # Return top N items
        return [item for item, _ in good_matches[:top_n]]
    
    def display_recommendations(self, items: List[ClothingItem], preferences: Dict[str, Any]) -> None:
        """Display recommended items to the user in a friendly format."""
        if not items:
            print("\n😔 Sorry, I couldn't find any items that match your preferences.")
            
            # Suggest relaxing some constraints
            print("\nTips for finding more items:")
            print("• Try selecting multiple seasons or occasions")
            print("• Be more flexible with color or style preferences")
            print("• Consider browsing all items in a specific category")
            return
        
        print(f"\n✨ FOUND {len(items)} RECOMMENDATIONS FOR YOU! ✨")
        
        # Show what preferences were used in the search
        print("\nBased on your preferences:")
        for attr, value in preferences.items():
            if value:
                if attr == "price_range" and preferences.get("price_range"):
                    min_price, max_price = preferences["price_range"]
                    max_str = f"${max_price:.2f}" if max_price != float('inf') else "no maximum"
                    print(f"• Price range: ${min_price:.2f} to {max_str}")
                elif isinstance(value, list):
                    print(f"• {attr.capitalize()}: {', '.join(value)}")
                else:
                    print(f"• {attr.capitalize()}: {value}")
        
        # Display each recommended item
        for i, item in enumerate(items, 1):
            print(f"\n[Recommendation #{i}]")
            item.display()
    
    def run(self) -> None:
        """Run the main application loop."""
        while True:
            print("\n" + "=" * 60)
            print("🛍️  THRIFT SHOP CLOTHING ASSISTANT 🛍️")
            print("=" * 60)
            print("1. Find clothing recommendations")
            print("2. Browse all items")
            print("3. View random item")
            print("4. Exit")
            
            choice = input("\nEnter your choice (1-4): ").strip()
            
            if choice == "1":
                preferences = self.gather_preferences()
                recommendations = self.recommend_items(preferences)
                self.display_recommendations(recommendations, preferences)
                
                # Ask if they want to save their results to a file
                save_choice = input("\nWould you like to save these recommendations to a file? (y/n): ").lower()
                if save_choice.startswith('y'):
                    filename = input("Enter filename (recommendations.json): ").strip() or "recommendations.json"
                    try:
                        with open(filename, 'w') as f:
                            json.dump([item.to_dict() for item in recommendations], f, indent=2)
                        print(f"Recommendations saved to {filename}")
                    except Exception as e:
                        print(f"Error saving recommendations: {e}")
                
            elif choice == "2":
                print("\n📋 ALL ITEMS IN INVENTORY 📋")
                for i, item in enumerate(self.items, 1):
                    print(f"\n[Item #{i}]")
                    item.display()
                    
                    # Pause after every 3 items
                    if i % 3 == 0 and i < len(self.items):
                        input("\nPress Enter to continue viewing items...")
            
            elif choice == "3":
                random_item = random.choice(self.items)
                print("\n🎲 RANDOM ITEM SHOWCASE 🎲")
                random_item.display()
                
            elif choice == "4":
                print("\nThank you for using the Thrift Shop Assistant! Come back soon! 👋")
                break
                
            else:
                print("\nInvalid choice. Please try again.")
            
            # Ask if they want to continue
            if choice != "4":
                continue_choice = input("\nWould you like to do something else? (y/n): ").lower()
                if not continue_choice.startswith('y'):
                    print("\nThank you for using the Thrift Shop Assistant! Come back soon! 👋")
                    break


if __name__ == "__main__":
    # Check if inventory file exists, otherwise use default
    inventory_file = "inventory.json"
    assistant = ThriftShopAssistant(inventory_file)
    
    try:
        assistant.run()
    except KeyboardInterrupt:
        print("\n\nProgram terminated by user. Goodbye!")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        print("The program will now exit.")
