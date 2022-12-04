def main():
    with open(file="sacks.xd", mode="r", encoding="utf-8") as fSacks:
        sackLines = fSacks.readlines()
        badgeValues = 0
        groupCount = 0
        for elfGroupStart in range(0,len(sackLines),3):
            elfGroupInventory = dict()
            elfGroup = sackLines[elfGroupStart:elfGroupStart+3]
            for elfSack in elfGroup:
                elfSackInventoryDeduped = set(elfSack.strip())
                for item in elfSackInventoryDeduped:
                    elfGroupItemCount = elfGroupInventory.get(item) or 0
                    elfGroupInventory.update({item: elfGroupItemCount+1})
            for item, quantity in elfGroupInventory.items():
                if quantity == 3:
                    badgeValue = ord(item)
                    if badgeValue > 90:
                        badgeValues+=(badgeValue-96)
                    else:
                        badgeValues+=(badgeValue-38)
        print(groupCount)
        print(badgeValues)
                    

if __name__ == "__main__":
    main()