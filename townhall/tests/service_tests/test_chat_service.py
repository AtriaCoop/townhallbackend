from django.test import TestCase
from django.contrib.auth.models import User
from myapi.services import chatServices
from myapi.models import Chat


class ChatServiceTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username="testuser1")
        self.user2 = User.objects.create(username="testuser2")
        self.chat = Chat.objects.create()  # Create a chat instance
        self.chat.participants.add(self.user1)

    # GET chat
    def test_get_chats_by_user_success(self):
        result = chatServices.get_chat(self.user1.id)
        self.assertEqual(result["message"], "Success")
        self.assertEqual(len(result["data"]), 1)

    def test_get_chats_no_user(self):
        result = chatServices.get_chat(999)
        self.assertEqual(result["error"], "User with ID 999 does not exist.")

    def test_get_chats_no_chats(self):
        another_user = User.objects.create(username="anotheruser")
        result = chatServices.get_chat(another_user.id)
        self.assertEqual(result["message"], "No chats found for this user")
        self.assertEqual(len(result["data"]), 0)

    # CREATE Chat
    def test_create_chat_success(self):
        result = chatServices.start_chat([self.user1.id, self.user2.id])
        self.assertEqual(result["message"], "Chat created successfully")
        self.assertIsInstance(result["data"], Chat)

    def test_create_duplicate_chat(self):
        # Create a chat between user1 and user2 first
        chatServices.start_chat([self.user1.id, self.user2.id])

    # DELETE Chat
    def test_delete_chat_success(self):
        # Create a chat to delete
        chat = chatServices.start_chat([self.user1.id, self.user2.id])["data"]
        result = chatServices.delete_chat(chat.id)
        self.assertEqual(result["message"], "Chat deleted successfully.")
        # Chat should no longer exist
        self.assertFalse(Chat.objects.filter(id=chat.id).exists())

    def test_delete_chat_invalid_id(self):
        result = chatServices.delete_chat(-1)  # Invalid ID
        self.assertEqual(result["error"], "Invalid chat ID provided.")

    def test_delete_chat_nonexistent(self):
        result = chatServices.delete_chat(999)  # Attempt to delete a non-existent chat
        self.assertEqual(result["error"], "Chat with ID 999 does not exist.")
