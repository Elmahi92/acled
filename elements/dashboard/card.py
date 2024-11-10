from streamlit_elements import mui
from .dashboard import Dashboard

class KPI_Card(Dashboard.Item):
    
    def __call__(
        self,
        content=None,
        default_content="No data available",
        title="KPI Title",
        subheader="Period: Q1 2024",
       # avatar_text="KPI",
       # avatar_color="blue",
        image_url=None,
        alt_text="KPI image",
        show_favorite=True,
        show_share=True,
        value=None,
        trend=None,  # A trend indicator (e.g., "up" or "down")
        progress=None,  # A progress value (between 0 and 100)
        width=350,
        height=400,
        top=0,
        left=0
    ):
        # Use provided content or fall back to default_content
        content = content if content is not None else default_content

        # Card container with configurable position and size
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
            elevation=1,
        ):
            mui.CardHeader(
                title=title,
                subheader=subheader,
               # avatar=mui.Avatar(avatar_text, sx={"bgcolor": avatar_color}),
                action=mui.IconButton(mui.icon.MoreVert),
                className=self._draggable_class,
            )
            # Optionally add an image for the KPI (e.g., logo or chart)
            if image_url:
                mui.CardMedia(
                    component="img",
                    height=194,
                    image=image_url,
                    alt=alt_text,
                )
            
            with mui.CardContent(sx={"flex": 1}):
                mui.Typography(content)

                # Render KPI value
                if value is not None:
                    mui.Typography(f"Value: {value}", variant="h5", sx={"fontWeight": "bold"})
                
                # Render trend (e.g., up or down)
                if trend:
                    trend_icon = mui.icon.TrendingUp if trend == "up" else mui.icon.TrendingDown
                    mui.Typography(f"Trend: {trend}", sx={"color": "green" if trend == "up" else "red"})
                    mui.IconButton(trend_icon)
                
                # Render progress bar if applicable
                if progress is not None:
                    mui.Typography(f"Progress: {progress}%", sx={"marginTop": 2})
                    mui.LinearProgress(value=progress/100)

            # Conditional rendering of actions
            with mui.CardActions(disableSpacing=True):
                if show_favorite:
                    mui.IconButton(mui.icon.Favorite)
                if show_share:
                    mui.IconButton(mui.icon.Share)
