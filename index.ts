import { config as loadEnv } from "dotenv";
import { config, higgsfield } from "@higgsfield/client/v2";

// Load HF_CREDENTIALS from .env.local without logging it.
loadEnv({ path: ".env.local", quiet: true });

const credentials = process.env.HF_CREDENTIALS;
if (!credentials || !credentials.includes(":")) {
  console.error("HF_CREDENTIALS is missing or not in key-id:key-secret format. Set it in .env.local.");
  process.exit(1);
}

// Video jobs can take longer than the SDK's 5-minute default polling window.
config({ credentials, maxPollTime: 15 * 60 * 1000 });

const MODEL = "bytedance/seedance-2.5/text-to-video";

async function main() {
  console.log(`Submitting ${MODEL}... (waiting for completion)`);

  const result = await higgsfield.subscribe(MODEL, {
    input: {
      prompt: "A cinematic scene at sunset",
      duration: 5,
      resolution: "720p",
      aspect_ratio: "16:9",
    },
    withPolling: true,
  });

  // The API may also report "canceled", which the SDK's type doesn't list.
  const status = result.status as string;

  if (status === "completed" && result.video?.url) {
    console.log(`Completed (request ${result.request_id})`);
    console.log(`Video URL: ${result.video.url}`);
    return;
  }

  const reason =
    status === "nsfw"
      ? "blocked by content moderation"
      : status === "failed"
        ? "generation failed"
        : status === "canceled" || status === "cancelled"
          ? "request was canceled"
          : status === "completed"
            ? "completed but no video URL was returned"
            : `ended with unexpected status "${status}"`;

  console.error(`Not successful (request ${result.request_id}): ${reason}.`);
  process.exitCode = 1;
}

main().catch((err: unknown) => {
  // Print only the error name/message; never dump config, which holds credentials.
  const e = err as { name?: string; message?: string };
  console.error(`Request error: ${e?.name ?? "Error"}: ${e?.message ?? String(err)}`);
  process.exitCode = 1;
});
