import random
from datetime import datetime, timedelta

class Product:
    def __init__(self, name, expdate):
        self.name = name
        self.expdate = expdate

    def __lt__(self, other): # less than
        return self.expdate < other.expdate

    def __str__(self): #output the result
        return f"{self.name}  | expire: {self.expdate:%Y-%m-%d}"

class Heap:
    def __init__(self):
        self.heap = []

    def add(self, product):
        self.heap.append(product)
        self.moveup(len(self.heap) - 1)

    def expSoonest(self):
        if not self.heap: #if nothing
            return None
        if len(self.heap) == 1: #if only one item
            return self.heap.pop()

        root = self.heap[0] #if two or more items
        self.heap[0] = self.heap.pop()
        self.movedown(0)
        return root

    def moveup(self, i):
        parent = (i - 1) // 2
        if i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self.moveup(parent)

    def movedown(self, i):
        smallest = i
        left, right = 2 * i + 1, 2 * i + 2

        if left < len(self.heap) and self.heap[left] < self.heap[smallest]:
            smallest = left
        if right < len(self.heap) and self.heap[right] < self.heap[smallest]:
            smallest = right

        if smallest != i:
            self.heap[i], self.heap[smallest] = self.heap[smallest], self.heap[i]
            self.movedown(smallest)

# Simulation
main = Heap()
# all items
items = ["Milk", "Eggs", "Bread", "Yogurt", "Chicken Breast", "Ground Beef", "Salmon", "Spinach", "Avocados", "Orange Juice", "Hummus", "Cottage Cheese", "Tofu", "Fresh Pasta", "Deli Turkey", "Sunscreen", "Mouthwash", "Eye Drops", "Contact Lens Solution", "Vitamin C Supplements", "Infant Formula", "Beer", "Wine", "Flour", "Dry Yeast", "Canned Soup", "Mayonnaise", "Salad Dressing", "Batteries", "Fire Extinguishers"]
today = datetime.now()

unsorted = [] # make an array for the unsorted list

for i in range(0, len(items)):
    name = items[i]
    expire = today + timedelta(days=random.randint(1, 60))
    product = Product(name, expire)
    
    unsorted.append(product) 
    main.add(product)

# display the unsorted list
print("The unsorted list:")
print("-" * 40)
for p in unsorted:
    print(p) # print the items in unsorted list

print("\n" + "="*40 + "\n")

# display the sorted list
print("The sorted list:")
print("-" * 40)
while main.heap:
    print(main.expSoonest()) #print the items in sorted list
