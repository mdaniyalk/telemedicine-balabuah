from dataclasses import dataclass
from datetime import datetime
from typing import Any




@dataclass
class Message:
    """
    Base Message Class in a chat.
    """
    message_id: str
    conversation_index: int
    timestamp: datetime
    message_type: str
    message_str: str
    
    def get_dict(self) -> dict[str, Any]:
        """
        Get the dict representation of the message.
        
        Returns:
            dict: The dict representation of the message.
        """
        timestamp_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "message_id": self.message_id,
            "conversation_index": self.conversation_index,
            "timestamp": timestamp_str,
            "message_type": self.message_type,
            "message_str": self.message_str
        }

    def get_message_dialogue(self) -> str:
        """
        Get the message string.
        
        Returns:
            str: The message string.
        """
        dialog = f"{self.message_type}: {self.message_str}"
        return dialog
    
    @classmethod
    def load_from_dict(cls, data: dict[str, Any]) -> 'Message':
        """
        Load a Message object from a dictionary.
        
        Args:
            data (dict): The dictionary containing the message data.
        
        Returns:
            Message: The Message object.
        """
        if isinstance(data["timestamp"], str):
            timestamp = datetime.strptime(data["timestamp"], "%Y-%m-%d %H:%M:%S")
        else:
            timestamp = data["timestamp"]
        return cls(
            message_id=data["message_id"],
            conversation_index=data["conversation_index"],
            timestamp=timestamp,
            message_type=data["message_type"],
            message_str=data["message_str"]
        )
    
