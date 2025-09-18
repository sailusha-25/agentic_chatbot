# core/mcp.py

import uuid

def create_mcp_message(sender, receiver, msg_type, payload=None):
    """
    Creates a structured message object following the Model Context Protocol (MCP).

    Args:
        sender (str): The name of the agent sending the message.
        receiver (str): The name of the agent intended to receive the message.
        msg_type (str): The type of the message (e.g., "INGEST_REQUEST", "CONTEXT_RESPONSE").
        payload (dict, optional): The data being sent. Defaults to None.

    Returns:
        dict: A dictionary representing the MCP message.
    """
    return {
        "sender": sender,
        "receiver": receiver,
        "type": msg_type,
        "trace_id": str(uuid.uuid4()),  # Generate a unique ID for tracking
        "payload": payload if payload is not None else {}
    }