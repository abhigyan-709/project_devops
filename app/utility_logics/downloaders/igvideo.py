# import instaloader

# def download_instagram_video(url, filename):
#     L = instaloader.Instaloader()
    
#     # Download the post (you can also pass a username if the post is private)
#     post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
    
#     # Download the video
#     L.download_post(post, target=filename)
#     print(f"Downloaded video to {filename}")

# # Example usage
# download_instagram_video("https://www.instagram.com/reel/DEteSBItfqe/?igsh=anZkYnBvZ252dzNj", "downloaded_video")

# app/utility_logics/downloaders/igvideo.py
import instaloader

def download_instagram_video(url: str, filename: str):
    try:
        L = instaloader.Instaloader()
        
        # Download the post (you can also pass a username if the post is private)
        post = instaloader.Post.from_shortcode(L.context, url.split("/")[-2])
        
        # Download the video
        L.download_post(post, target=filename)
        return f"Downloaded video to {filename}"
    except Exception as e:
        raise Exception(f"Error downloading video: {str(e)}")
