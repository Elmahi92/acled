from streamlit_elements import mui
from .dashboard import Dashboard

class HeaderCard(Dashboard.Item):
    def __call__(
        self,
        title="Header Title",
        subtitle="Subtitle Text",
        body_text="This is the body text. You can include additional details here.",
        media_url="https://example.com/your-media-url.jpg",  # URL to the image or video
        alt_text="Alternative Text for Media",
        width=800,
        height=200,
        top=0,
        left=0
    ):
        # Card container for the header
        with mui.Card(
            key=self._key,
            sx={
                "display": "flex",
                "flexDirection": "column",
                "borderRadius": 3,
                "overflow": "hidden",
                "width": width,
                "height": height,
                "position": "absolute",
                "top": top,
                "left": left,
            },
            elevation=3,  # You can adjust elevation for shadow depth
        ):
            mui.CardHeader(
                title=title,
                subheader=subtitle,
                sx={"textAlign": "center"},
            )
            
            # Add media (image or video)
            mui.CardMedia(
                component="img",  # Change to 'video' if necessary
                height=300,  # Adjust height as needed
                image=media_url,
                alt=alt_text,
                sx={"objectFit": "cover"}  # Ensure media covers the area
            )

            # Add body content (text) for the header
            with mui.CardContent(sx={"flex": 1, "textAlign": "center"}):
                mui.Typography(body_text)
