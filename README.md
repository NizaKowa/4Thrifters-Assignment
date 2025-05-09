# 4Thrifters-Assignment

A Python command-line application that recommends thrifted clothing items based on user preferences.

## Personal Information

- **Name:** Niza Kowa
- **Email:** nizakowa15@gmail.com

## How to Run

1. Make sure you have Python 3.6+ installed
2. Save the `thrift_shop_assistant.py` file to your local system
3. Run the script:

```
python thrift_shop_assistant.py
```

No external libraries are required as this application uses only Python's standard library.

## Thought Process and Design Choices

When approaching this project, I focused on creating an intuitive and helpful shopping assistant that would feel like talking to a knowledgeable thrift store employee. Here's my thought process:

### Data Modeling Strategy
I designed a comprehensive data model that captures the unique aspects of thrifted clothing. Unlike new retail items, thrifted pieces vary in condition, era, and uniqueness. My `ClothingItem` class reflects this with attributes for condition, style, and detailed descriptions.

### User Experience Philosophy
I aimed for a conversational interface that guides users without overwhelming them:
- Questions are presented one at a time
- Options are always shown when available
- Users can skip any question to keep the experience flexible
- Fuzzy matching ensures users don't need to type exact matches

### Recommendation Algorithm Approach
For the matching system, I created a weighted scoring algorithm that:
- Gives higher importance to fundamental attributes (category, gender)
- Uses fuzzy text matching for string comparisons
- Handles partial matches for list attributes like seasons or occasions
- Normalizes scores so users aren't penalized for skipping questions

This creates recommendations that feel intuitive and helpful rather than rigidly rules-based.

## Bonus Features Added

1. **OOP Structure**:
   - Used Python's `dataclass` for a clean `ClothingItem` implementation with proper type hints
   - Organized code with clear class responsibilities and encapsulation

2. **Interactive Multi-level CLI**:
   - Main menu with multiple exploration options
   - Browse all items with pagination (pause after every 3 items)
   - Random item discovery feature for serendipitous finds
   - Option to continue shopping or exit after each action

3. **Advanced Recommendation System**:
   - Weighted attribute importance based on shopping psychology
   - Normalized scoring to ensure fair comparisons
   - Minimum threshold filtering to only show quality matches
   - Helpful suggestions when no matches are found

4. **Data Persistence**:
   - Support for loading custom inventory from JSON files
   - Option to save recommendations to a file for later reference
   - Error handling for file operations

5. **Robust Error Management**:
   - Comprehensive input validation
   - Graceful handling of unexpected inputs
   - Clear error messages with recovery paths
