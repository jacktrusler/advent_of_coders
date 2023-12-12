from __future__ import annotations
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    """
    Represents an interval of integers.
    
    This class acts as "storage" for numbers ranging from a start to an end. While all of the digits 
    inside of this range are within it, they are not ever stored. This allows the class to work well
    with representing intervals of larger numbers. Much of the behavior is modeled after sets.

    start : int : The first integer of the interval
    end   : int : The last integer of the interval
    """
    start: int
    end: int

    def __hash__(self):
        return hash((self.start, self.end))

    def __add__(self, val: int) -> Interval:
        """
        Add the given value to both the start and end of the interval
        """
        return Interval(start=self.start + val, end=self.end + val)
    
    def __radd__(self, val: int) -> Interval:
        """
        Add the given value to both the start and end of the interval
        """
        return self + val
    
    def __sub__(self, val: int) -> Interval:
        """
        Subtract the given value from both the start and end of the interval
        """
        return Interval(start=self.start - val, end=self.end - val)
    
    def __rsub__(self, val: int) -> Interval:
        """
        Subtract the start and end of the interval from the given value
        """
        return Interval(start=val - self.start, end=val - self.end)
    
    def __contains__(self, val: int | Interval) -> bool:
        """
        Check if there is any overlap between this interval and the given int/interval value
        """
        match val:
            case int(): return self.start <= val <= self.end
            case Interval(): return self.start <= val.end and self.end >= val.start
    
    def __lt__(self, val: int | Interval) -> bool:
        """
        If the given value is an int, check if all values of the interval are less than the value.
        Otherwise, check if the given interval is a sub-interval of this interval.
        """
        match val:
            case int(): return self.end < val
            case Interval(): return self.start >= val.start and self.end <= val.end

    def __rt__(self, val: int | Interval) -> bool:
        """
        If the given value is an int, check if all values of the interval are greater than the value.
        Otherwise, check if the given interval is a super-interval of this interval.
        """
        match val:
            case int(): return self.start > val
            case Interval(): return self.start <= val.start and self.end >= val.end

    def __len__(self):
        """
        Get the number of digits in the interval
        """
        return self.end - self.start + 1
    
    def __and__(self, val: int | Interval) -> int | Interval:
        """
        Get all shared values between this interval and the passed in value
        """
        match val:
            case int(): return val if val in self else 0
            case Interval(): return self.intersection(val)
    
    def __iter__(self):
        """
        Iterate over all values in the interval
        """
        return iter(range(self.start, self.end + 1))
    
    def intersection(self, other: Interval) -> Interval:
        """
        The intersection of two intervals is all of the values they have in common
        """
        if self not in other:
            return None
        return Interval(
            start = max(self.start, other.start),
            end = min(self.end, other.end),
        )
    
    def difference(self, other: Interval) -> list[Interval]:
        """
        The difference between this interval and another are all of the values this interval has
        that the other does not.
        
        These values could be an interval starting to the left of the other interval, an interval
        starting to the right of the other interval, or neither. Thus, a list of intervals is returned.
        """
        retval = []
        if self < other or self not in other:
            return []
        if self.start not in other:
            retval.append(Interval(self.start, other.start - 1))
        if self.end not in other:
            retval.append(Interval(other.end + 1, self.end))
        return retval
    
    def union(self, other: Interval) -> Interval:
        """
        The union of two intervals is an interval that spans both of them, if possible.
        This only will be possible if there is no gap between them.
        """
        if (other.start - self.end) > 1:
            return None
        return Interval(
            start = min(self.start, other.start),
            end = max(self.end, other.end)
        )
