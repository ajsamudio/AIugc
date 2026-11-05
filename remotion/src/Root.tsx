import { Composition } from "remotion";
import { ColorBroll, colorBrollDuration, type ColorBrollProps } from "./ColorBroll";

// Tiff · Day 1 · YEOREO Sophie set, listing photos in six colors
const d01: ColorBrollProps = {
  photos: [
    { src: "d01/black.jpg", name: "black", swatch: "#1d1d1f" },
    { src: "d01/dark_brown.jpg", name: "dark brown", swatch: "#4a3328" },
    { src: "d01/pink.jpg", name: "pink", swatch: "#f2b8c6" },
    { src: "d01/dark_green.jpg", name: "dark green", swatch: "#2f7a4e" },
    { src: "d01/navy.jpg", name: "navy", swatch: "#26355e" },
    { src: "d01/anchor_red.jpg", name: "red", swatch: "#9e2b37" },
  ],
  headline: "13 colors",
};

export const Root: React.FC = () => (
  <Composition
    id="d01-color-broll"
    component={ColorBroll}
    defaultProps={d01}
    durationInFrames={colorBrollDuration(d01.photos.length)}
    fps={30}
    width={720}
    height={1280}
  />
);
