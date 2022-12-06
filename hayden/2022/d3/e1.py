def main():
    with open(file="sacks.xd", mode="r", encoding="utf-8") as fSacks:
        sackLines = fSacks.readlines()
        itemValues = 0
        for sackLine in sackLines:
            sackSplit = (len(sackLine)+1)//2
            leftSack = sackLine[:sackSplit-1]
            rightSack = sackLine[sackSplit-1:]
            commonItemInSacks = ''
            for item in leftSack:
                if commonItemInSacks:
                    break
                for comparedItem in rightSack:
                    if item == comparedItem:
                        commonItemInSacks = item
                        break

            if commonItemInSacks:
                itemValue = ord(commonItemInSacks)
                if itemValue > 90:
                    itemValues+=(itemValue-96)
                else:
                    itemValues+=(itemValue-38)
        print(itemValues)
            
                        

if __name__ == "__main__":
    main()