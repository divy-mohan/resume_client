from flask_socketio import emit, join_room, leave_room
from flask_login import current_user
from app import socketio, db
from models import ChatMessage, Order

@socketio.on('connect')
def on_connect():
    if current_user.is_authenticated:
        emit('status', {'msg': f'{current_user.get_full_name()} has connected'})

@socketio.on('disconnect')
def on_disconnect():
    if current_user.is_authenticated:
        emit('status', {'msg': f'{current_user.get_full_name()} has disconnected'})

@socketio.on('join')
def on_join(data):
    if current_user.is_authenticated:
        room = f"order_{data['order_id']}"
        join_room(room)
        emit('status', {'msg': f'{current_user.get_full_name()} has joined the chat'}, room=room)

@socketio.on('leave')
def on_leave(data):
    if current_user.is_authenticated:
        room = f"order_{data['order_id']}"
        leave_room(room)
        emit('status', {'msg': f'{current_user.get_full_name()} has left the chat'}, room=room)

@socketio.on('message')
def handle_message(data):
    if not current_user.is_authenticated:
        return
    
    order_id = data.get('order_id')
    message_text = data.get('message')
    
    # Verify user has access to this order
    order = Order.query.filter_by(id=order_id, user_id=current_user.id).first()
    if not order:
        return
    
    # Save message to database
    message = ChatMessage(
        user_id=current_user.id,
        order_id=order_id,
        message=message_text,
        is_admin=current_user.is_admin
    )
    db.session.add(message)
    db.session.commit()
    
    # Emit message to room
    room = f"order_{order_id}"
    emit('message', {
        'message': message_text,
        'user_name': current_user.get_full_name(),
        'is_admin': current_user.is_admin,
        'timestamp': message.created_at.isoformat()
    }, room=room)

@socketio.on('typing')
def handle_typing(data):
    if current_user.is_authenticated:
        room = f"order_{data['order_id']}"
        emit('typing', {
            'user_name': current_user.get_full_name(),
            'is_typing': data['is_typing']
        }, room=room, include_self=False)
