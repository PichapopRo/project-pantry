"""Status for the recipe."""
from enum import Enum


class StatusCode(Enum):
    """The status of the recipe approval."""

    APPROVE = ("approved", "Approved")
    PENDING = ("pending", "Pending")
    REJECTED = ("rejected", "Rejected")
    
    @classmethod
    def get_choice(cls) -> list[tuple[str, str]]:
        """
        Get the choice set for the recipe model.
        
        :return: The list of tuples to be input into choices.
        """
        statuses = []
        for status in StatusCode:
            statuses.append((status.value[0], status.value[1]))
        return statuses


# Example usage
if __name__ == "__main__":
    status_code = StatusCode
    choices = status_code.get_choice()
    print(choices)
    print(StatusCode.APPROVE.value[0])
    
    for status in StatusCode:
        print(status)
