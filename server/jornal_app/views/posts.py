from rest_framework.generics import GenericAPIView, ListAPIView
from server.jornal_app.api.permissions import IsUser
from server.jornal_app.models.posts import Post
from server.jornal_app.serializers.posts import *
from server.jornal_app.api.response import CustomResponse
from server.jornal_app.services.posts import *

# Make Post, Comment and Reply -> Methods = POST
class MakePostApiVeiw(GenericAPIView):
    """Make post by user"""
    permission_classes = [IsUser,]
    serializer_class = CustomPostSerializer
    def post(self, request, format=None):
        serializer = CustomPostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            return CustomResponse.success(message="Post was published", data=serializer.data)
        return CustomResponse.bad_request(
            message="Can not publish this post, please check your data and send it again", 
            error=serializer.errors
        )

class MakeCommentOnPostApiVeiw(GenericAPIView):
    """Post comment on post endpoint"""
    permission_classes = [IsUser,]
    serializer_class = CustomCommentSerializer
    def post(self, request, format=None):
        post = get_post_by_id(request.data.get('post'))
        if post:
            serializer = CustomCommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author = request.user, post = post)
                return CustomResponse.success(message="Comment Details", data = serializer.data)
            return CustomResponse.bad_request(
                message="Can not publish this comment, please check your data and send it again",
                error=serializer.errors
                )
        return CustomResponse.not_found(message = f"Comment with id {id}, not found")

class MakeReplyOnCommentApiVeiw(GenericAPIView):
    """Post reply on comment endpoint"""
    permission_classes = [IsUser,]
    serializer_class = CommentReplySerializer
    def post(self, request, format=None):
        comment = get_comment_by_id(request.data.get('comment'))
        if comment:
            serializer = CommentReplySerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=request.user, comment=comment)
                return CustomResponse.success(message="Reply Details", data=serializer.data)
            return CustomResponse.bad_request(
                message="Can not publish this reply, please check your data and send it again",
                error=serializer.errors
                )
        return CustomResponse.not_found(message = f"Comment with id {id}, not found")

# Get Post, Comment and Reply -> Methods = GET
class GetPostByIdApiVeiw(GenericAPIView):
    """Get post by id api endpoint"""
    permission_classes = [IsUser,]
    serializer_class = CustomPostSerializer
    def get(self, request, id, format=None):
        post = get_post_by_id(id)
        if post:
            serializer = CustomPostSerializer(post)
            return CustomResponse.success(message="Post Details", data = serializer.data)
        return CustomResponse.not_found(message =f"Can not found post with id {id}")

class GetCommentByIdApiVeiw(GenericAPIView):
    """Get comment by id api endpoint"""
    permission_classes = [IsUser,]
    def get(self, request, id, format=None):
        comment = get_comment_by_id(id)
        if comment:
            serializer = CommentSerializer(comment)
            return CustomResponse.success(message="Comment Details", data = serializer.data)
        return CustomResponse.not_found(message =f"Can not found comment with id {id}")

class GetReplyByIdApiVeiw(GenericAPIView):
    """Get reply by id api endpoint"""
    permission_classes = [IsUser,]
    def get(self, request, id, format=None):
        reply = get_reply_by_id(id)
        if reply:
            serializer = CommentReplySerializer(reply)
            return CustomResponse.success(message="Reply Details", data = serializer.data)
        return CustomResponse.not_found(message =f"Can not found reply with id {id}")

class AllMyPostsListApiVeiw(ListAPIView):
    """Get all posts"""
    permission_classes = [IsUser,]
    def get(self, request, format=None):
        posts = Post.objects.filter(author = request.user).select_related('author')
        try:
            return CustomResponse.success(message="Success Response",data = CustomPostSerializer(posts, many=True).data)
        except:
            return CustomResponse.bad_request(message = "Get requests error, Server request error")

# Update Post, Comment and Reply -> Methods = Put
class UpdatePostApiVeiw(GenericAPIView):
    """Update post by id api endpoint"""
    permission_classes = [IsUser,]
    serializer_class = CustomPostSerializer
    def put(self, request, id, format=None):
        post = get_post_by_id(id)
        if post:
            if request.user.id == post.author.id:
                serializer = CustomPostSerializer(post, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return CustomResponse.success(message="Update Post Details", data = serializer.data)
                return CustomResponse.bad_request(message="Make Sure that you entered a valid data")
            return CustomResponse.bad_request(message="You dont have access to update this post")
        return CustomResponse.not_found(message="We're trying to get this post but cannot")

class UpdateCommentApiVeiw(GenericAPIView):
    """Update comment by id api endpoint"""
    permission_classes = [IsUser,]
    serializer_class = CommentSerializer
    def put(self, request, id, format=None):
        comment = get_comment_by_id(id)
        if comment:
            if request.user.id == comment.author.id:
                serializer = CommentSerializer(comment, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return CustomResponse.success(message="Update Comment Details", data = serializer.data)
                return CustomResponse.bad_request(message="Make Sure that you entered a valid data", error=serializer.errors)
            return CustomResponse.bad_request(message="You dont have access to update this comment")
        return CustomResponse.not_found(message="We're trying to get this comment but cannot")

class UpdateReplyApiVeiw(GenericAPIView):
    """Update reply by id api endpoint"""
    permission_classes = [IsUser,]
    serializer_class = CommentReplySerializer
    def put(self, request, id, format=None):
        reply = get_reply_by_id(id)
        if reply:
            if request.user.id == reply.author.id:
                serializer = CommentReplySerializer(reply, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return CustomResponse.success(message="Update Comment Reply Details", data = serializer.data)
                return CustomResponse.bad_request(message="Make Sure that you entered a valid data", error=serializer.errors)
            return CustomResponse.bad_request(message="You dont have access to update this reply")
        return CustomResponse.not_found(message=f"Reply with id {id} not found")

# Delete Post, Comment and Reply -> Methods = DELETE
class DeletePostApiVeiw(GenericAPIView):
    """Delete post by id"""
    permission_classes = [IsUser,]
    def delete(self, request, id, format=None):
        post = get_post_by_id(id)
        if post:
            post.delete()
            return CustomResponse.success(message="Post removed", data = {}, status_code=204)
        return CustomResponse.not_found(message = f"Post with id {id}, not found")

class DeleteCommentApiVeiw(GenericAPIView):
    """Delete comment by id"""
    permission_classes = [IsUser,]
    def delete(self, request, id, format=None):
        comment = get_comment_by_id(id)
        if comment:
            comment.delete()
            return CustomResponse.success(message="Comment removed", data = {}, status_code=204)
        return CustomResponse.not_found(message = f"Comment with id {id}, not found")

class DeleteReplyApiVeiw(GenericAPIView):
    """Delete reply by id"""
    permission_classes = [IsUser,]
    def delete(self, request, id, format=None):
        reply = get_reply_by_id(id)
        if reply:
            reply.delete()
            return CustomResponse.success(message="Reply removed", data = {}, status_code=204)
        return CustomResponse.not_found(message = f"Reply with id {id}, not found")

# Action Post, Comment and Reply -> Methods = POST
class LikePostApiVeiw(GenericAPIView):
    """Make like to post endpoint"""
    permission_classes = [IsUser,]
    def post(self, request, id, format=None):
        post = get_post_by_id(id)
        serializer = CustomPostSerializer(post).data
        if post:
            arr = [user.id for user in post.likes.all()]
            if request.user.id in arr:
                post.likes.remove(request.user)
            else:
                post.likes.add(request.user)
            return CustomResponse.success(message="Post Details", data = serializer)
        return CustomResponse.not_found(message = f"Post with id {id}, not found")

class LikeCommentPostApiVeiw(GenericAPIView):
    """Make like to comment endpoint"""
    permission_classes = [IsUser,]
    def post(self, request, id, format=None):
        comment = get_comment_by_id(id)
        if comment:
            arr = [user.id for user in comment.likes.all()]
            if request.user.id in arr:
                comment.likes.remove(request.user)
            else:
                comment.likes.add(request.user)
            return CustomResponse.success(message="Comment Details", data = CustomCommentSerializer(comment).data)
        return CustomResponse.not_found(message = f"Comment with id {id}, not found")

class LikeReplyPostApiVeiw(GenericAPIView):
    """Make like to comment endpoint"""
    permission_classes = [IsUser,]
    def post(self, request, id, format=None):
        reply = get_reply_by_id(id)
        if reply:
            arr = [user.id for user in reply.likes.all()]
            if request.user.id in arr:
                reply.likes.remove(request.user)
            else:
                reply.likes.add(request.user)
            return CustomResponse.success(message="Reply Details", data = CommentReplySerializer(reply).data)
        return CustomResponse.not_found(message = f"Reply with id {id}, not found")

class SherePostApiVeiw(GenericAPIView):
    """Make post by user"""
    permission_classes = [IsUser,]
    serializer_class = CustomPostSerializer
    def post(self, request, format=None):
        serializer = CustomPostSerializer(data=request.data)
        if serializer.is_valid():
            shered_post = request.data.get('shered_post')
            standerd_post = get_post_by_id(shered_post)
            if standerd_post:
                this_post = serializer.save(author = request.user, shered_post = standerd_post)
                return CustomResponse.success(message="Post was published", data = CustomPostSerializer(this_post).data)
        return CustomResponse.bad_request(message = "Can not publish this post, please check your data and send it again")

class PostTransleatorByIdApiVeiw(GenericAPIView):
    """translate post to user lang"""
    permission_classes = [IsUser,]
    def get(self, request, id, code, format=None):
        post = get_post_by_id(id)
        if post:
            return CustomResponse.success(message="Post Details", data = custom_translate_response(post, code))
        return CustomResponse.not_found(message = f"Post with id {id}, not found")

class AddPostToBookmarksAPIView(GenericAPIView):
    """By using this endpoint you can save,unsave more than one post to your bookmarks"""
    permission_classes = [IsUser,]
    def post(self, request, post_id, format=None):
        """Add post to bookmarks"""
        bookmark = get_or_creqate_bookmark_by_user(request.user)
        post = get_post_by_id(int(post_id))
        if post:
            bookmark.posts.add(post)
            return CustomResponse.success(message='Post saved successfully')
        return CustomResponse.not_found(message='There are no post with this id.')
    
class GetMyBookMarksAPIView(ListAPIView):
    """Get bookmark posts based on the request user"""
    permission_classes = [IsUser,]
    serializer_class = CustomPostSerializer
    def get_queryset(self):
        """Get Bookmarks"""
        posts = get_posts_from_bookmark_based_on_user(self.request.user)
        print(posts)
        if posts:
            return posts
        return CustomResponse.not_found(message = "There are no bookmarks to this user.")

class RemovePostFromBookMarksAPIView(GenericAPIView):
    """Delete post from bookmark posts"""
    permission_classes = [IsUser,]
    def delete(self, request, post_id):
        """Delete post from bookmark posts"""
        bookmark = get_bookmark_by_user(request.user)
        if bookmark:
            post = get_post_by_id(int(post_id))
            if post and post in bookmark.posts.all():
                bookmark.posts.remove(post)
                return CustomResponse.success(message='Post removed successfully')
            return CustomResponse.not_found(message = "Can not find any post in your bookmark with this id")
        return CustomResponse.not_found(message = "There are no bookmarks to this user.")