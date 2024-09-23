from gcms import GCMS
from object import Color
from exceptions import NoBinFoundException

def print_separator():
    print("\n" + "-"*80 + "\n")

if __name__ == "__main__":
    # Initialize GCMS
    gcms = GCMS()
    
    # Adding an initial set of bins with varying capacities
    initial_bin_data = [
        (1001, 50),
        (1002, 30),
        (1003, 40),
        (1004, 25),
        (1005, 35),
        (1006, 60),
        (1007, 45),
        (1008, 55),
        (1009, 20),
        (1010, 70)
    ]
    
    print("Adding Initial Bins:")
    for bin_id, capacity in initial_bin_data:
        gcms.add_bin(bin_id, capacity)
        print(f"Added Bin ID: {bin_id}, Capacity: {capacity}")
    
    print_separator()
    
    # Adding an initial set of objects with varying sizes and colors
    initial_object_data = [
        (2001, 20, Color.RED),
        (2002, 15, Color.YELLOW),
        (2003, 10, Color.BLUE),
        (2004, 25, Color.GREEN),
        (2005, 30, Color.RED),
        (2006, 5, Color.YELLOW),
        (2007, 8, Color.BLUE),
        (2008, 22, Color.GREEN),
        (2009, 35, Color.BLUE),
        (2010, 40, Color.RED),
        (2011, 12, Color.YELLOW),
        (2012, 18, Color.GREEN),
        (2013, 7, Color.BLUE),
        (2014, 28, Color.RED),
        (2015, 16, Color.YELLOW)
    ]
    
    print("Adding Initial Objects:")
    for obj_id, size, color in initial_object_data:
        try:
            gcms.add_object(obj_id, size, color)
            print(f"Added Object ID: {obj_id}, Size: {size}, Color: {color.name}")
        except NoBinFoundException:
            print(f"Failed to add Object ID: {obj_id}, Size: {size}, Color: {color.name} - No suitable bin found")
    
    print_separator()
    
    # Displaying bin information after initial additions
    print("Bin Information After Adding Initial Objects:")
    for bin_id, _ in initial_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()
    
    # Displaying object information after initial additions
    print("Object Information After Adding Initial Objects:")
    for obj_id, _, _ in initial_object_data:
        try:
            assigned_bin = gcms.object_info(obj_id)
            print(f"Object ID: {obj_id} is assigned to Bin ID: {assigned_bin}")
        except Exception as e:
            print(f"Error retrieving info for Object ID: {obj_id} - {str(e)}")
    
    print_separator()
    
    # Adding additional bins after some objects have been placed
    additional_bin_data = [
        (1011, 65),
        (1012, 45),
        (1013, 55)
    ]
    
    print("Adding Additional Bins:")
    for bin_id, capacity in additional_bin_data:
        gcms.add_bin(bin_id, capacity)
        print(f"Added Bin ID: {bin_id}, Capacity: {capacity}")
    
    print_separator()
    
    # Adding additional objects after new bins have been added
    additional_object_data = [
        (2016, 25, Color.GREEN),
        (2017, 14, Color.YELLOW),
        (2018, 9, Color.BLUE),
        (2019, 50, Color.RED),
        (2020, 33, Color.YELLOW),
        (2021, 12, Color.GREEN),
        (2022, 7, Color.BLUE),
        (2023, 19, Color.RED),
        (2024, 28, Color.YELLOW),
        (2025, 11, Color.BLUE)
    ]
    
    print("Adding Additional Objects:")
    for obj_id, size, color in additional_object_data:
        try:
            gcms.add_object(obj_id, size, color)
            print(f"Added Object ID: {obj_id}, Size: {size}, Color: {color.name}")
        except NoBinFoundException:
            print(f"Failed to add Object ID: {obj_id}, Size: {size}, Color: {color.name} - No suitable bin found")
    
    print_separator()
    
    # Displaying bin information after adding additional objects
    print("Bin Information After Adding Additional Objects:")
    for bin_id, _ in initial_bin_data + additional_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()
    
    # Displaying object information after adding additional objects
    print("Object Information After Adding Additional Objects:")
    for obj_id, _, _ in initial_object_data + additional_object_data:
        try:
            assigned_bin = gcms.object_info(obj_id)
            print(f"Object ID: {obj_id} is assigned to Bin ID: {assigned_bin}")
        except Exception as e:
            print(f"Object ID: {obj_id} has been deleted or does not exist - {str(e)}")
    
    print_separator()
    
    # Deleting some objects
    objects_to_delete = [2003, 2005, 2010, 2015, 2018, 2019] 
    print("Deleting Objects:")
    for obj_id in objects_to_delete:
        try:
            gcms.delete_object(obj_id)
            print(f"Deleted Object ID: {obj_id}")
        except Exception as e:
            print(f"Failed to delete Object ID: {obj_id} - {str(e)}")
    
    print_separator()
    
    # Displaying bin information after deletions
    print("Bin Information After Deleting Objects:")
    for bin_id, _ in initial_bin_data + additional_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()

    # Displaying object information after deletions
    print("Object Information After Deleting Objects:")
    current_items = initial_object_data + additional_object_data

    current_items = [ elt for elt, _, _ in current_items] 
    current_items = [elt for elt in current_items if elt not in objects_to_delete]
    for obj_id in current_items:
        try:
            assigned_bin = gcms.object_info(obj_id)
            print(f"Object ID: {obj_id} is assigned to Bin ID: {assigned_bin}")
        except Exception as e:
            print(f"Object ID: {obj_id} has been deleted or does not exist - {str(e)}")
    
    print_separator()
    
    # Attempting to add an object that cannot fit into any bin
    print("Adding an Object That Cannot Fit into Any Bin:")
    try:
        gcms.add_object(2026, 100, Color.BLUE)
        print(f"Added Object ID: 2026, Size: 100, Color: BLUE")
    except NoBinFoundException:
        print("Failed to add Object ID: 2026, Size: 100, Color: BLUE - No suitable bin found")
    
    print_separator()
    
    # Final bin information
    print("Final Bin Information:")
    for bin_id, _ in initial_bin_data + additional_bin_data:
        try:
            remaining_capacity, objects_in_bin = gcms.bin_info(bin_id)
            print(f"Bin ID: {bin_id}, Remaining Capacity: {remaining_capacity}, Objects: {objects_in_bin}")
        except Exception as e:
            print(f"Error retrieving info for Bin ID: {bin_id} - {str(e)}")
    
    print_separator()
    
    print("All enhanced tests completed.")