from .models import Category, DirectMessage

def user_messages(request):
    if request.user.is_authenticated:
        user_messages = DirectMessage.objects.filter(receiver=request.user)
        read_messages = [message for message in user_messages if message.is_read]
        unread_messages = DirectMessage.objects.filter(receiver=request.user, is_read=False)
        return {'user_messages': user_messages, 'read': read_messages, 'unread': unread_messages}
    return {}

def get_categories(request):
    categories = Category.objects.all()
    return {'categories': categories}