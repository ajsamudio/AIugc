import { AbsoluteFill, Easing, Img, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { TransitionSeries, springTiming } from "@remotion/transitions";
import { slide } from "@remotion/transitions/slide";
import { fade } from "@remotion/transitions/fade";

export type ColorBrollProps = {
  photos: { src: string; name: string; swatch: string }[];
  headline: string;
};

// ~1.3s of each photo on screen; transitions overlap neighbours
const HOLD = 46;
const TRANSITION = 16;
export const colorBrollDuration = (n: number) => n * HOLD - (n - 1) * TRANSITION;

const BG = "#ebebeb";
const timing = springTiming({ config: { damping: 200 }, durationInFrames: TRANSITION });

// Alternate the motion so the sequence doesn't feel like a slideshow
const presentations = [slide({ direction: "from-right" }), fade(), slide({ direction: "from-bottom" })];

const Photo: React.FC<{ src: string; name: string; swatch: string }> = ({ src, name, swatch }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  // Slow push-in for the whole time the photo is visible
  const scale = interpolate(frame, [0, HOLD], [1.0, 1.07], { extrapolateRight: "clamp", easing: Easing.out(Easing.quad) });
  const label = spring({ frame: frame - 6, fps, config: { damping: 200 } });
  return (
    <AbsoluteFill style={{ backgroundColor: BG, justifyContent: "center", alignItems: "center" }}>
      <Img src={staticFile(src)} style={{ width: 720, height: 720, transform: `scale(${scale})` }} />
      <div
        style={{
          position: "absolute",
          bottom: 250,
          display: "flex",
          alignItems: "center",
          gap: 14,
          padding: "12px 24px",
          borderRadius: 999,
          backgroundColor: "rgba(255,255,255,0.9)",
          fontFamily: "Georgia, serif",
          fontSize: 38,
          color: "#2a1e1a",
          opacity: label,
          transform: `translateY(${(1 - label) * 24}px)`,
        }}
      >
        <span style={{ width: 30, height: 30, borderRadius: 15, backgroundColor: swatch, border: "2px solid #fff" }} />
        {name}
      </div>
    </AbsoluteFill>
  );
};

export const ColorBroll: React.FC<ColorBrollProps> = ({ photos, headline }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const head = spring({ frame, fps, config: { damping: 200 } });
  return (
    <AbsoluteFill style={{ backgroundColor: BG }}>
      <TransitionSeries>
        {photos.flatMap((p, i) => {
          const seq = (
            <TransitionSeries.Sequence key={p.src} durationInFrames={HOLD}>
              <Photo {...p} />
            </TransitionSeries.Sequence>
          );
          if (i === photos.length - 1) return [seq];
          return [
            seq,
            <TransitionSeries.Transition key={`t${i}`} presentation={presentations[i % presentations.length]} timing={timing} />,
          ];
        })}
      </TransitionSeries>
      <div
        style={{
          position: "absolute",
          top: 190,
          width: "100%",
          textAlign: "center",
          fontFamily: "Georgia, serif",
          fontStyle: "italic",
          fontSize: 64,
          color: "#2a1e1a",
          opacity: head,
          transform: `scale(${interpolate(head, [0, 1], [0.92, 1])})`,
        }}
      >
        {headline}
      </div>
    </AbsoluteFill>
  );
};
