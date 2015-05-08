import videos
import youtubers

vid1 = videos.Video("https://www.youtube.com/watch?v=sGHAxbSEBZs")

vid2 = videos.Video("https://www.youtube.com/watch?v=sGHAxbSEBZs")

print vid1.title

vidlist = [vid1, vid2]
youtubers.write_movies_page(vidlist)