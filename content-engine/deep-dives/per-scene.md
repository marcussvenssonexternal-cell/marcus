# The next per-title moment: a scene-level content layer

_streaming technology · for tier-1 streamers, telco / cable operators, broadcasters, ad-funded streamers (AVOD / FAST)_

**Streaming made delivery content-aware with per-title and per-shot encoding. Ad breaks, artwork, previews and discovery still run on content-blind defaults; the next step is a scene-level content layer computed once at ingest that every downstream system reads.**

## Why now

Ad-supported streaming is 46.6% of ad-supported TV viewing (Nielsen, Q1 2026), ad loads rose about 18% this year (Ampere), and library is almost four in five hours of US TV streaming (Luminate, H1 2026). StreamingMeme invited Vionlabs to publish in its new Industry Voices section.

## Questions the series answers

- Why did per-title encoding spread so fast, and what does that teach us?
- Which decisions after delivery are still content-blind?
- What does a scene-level content layer contain and where does it sit?
- What are the honest objections?
- What should a platform measure first?

## What Vionlabs brings

Ad-break detection run in SDVI's Rally with operator validation; Fingerprint+ metadata (v11.15 vocabulary rebuild); Curio personalization on multimodal embeddings, live with Great American Pure Flix; the AWS Marketplace listing.

## Get before publishing

- StreamingMeme's Industry Voices rules: length, images, exclusivity and canonical links (we couldn't open the site from this session)
- Arash to confirm the webinar anecdote and the per-team section read the way he'd say them

## Series plan

1. **Streaming's next per-title moment won't happen in the encoder** (Guest article (StreamingMeme), Industry Trend Commentary)

## Evidence

- [Netflix: Per-Title Encode Optimization (via The Register)](https://www.theregister.com/2015/12/16/netflix_per_title_encode_optimization/) (2015-12-16)
- [Netflix: The Power of a Picture](https://about.netflix.com/en/news/the-power-of-a-picture) (2016-05-03)
- [Luminate 2026 Midyear Report](https://luminatedata.com/wp-content/uploads/2026/07/Midyear-REPORT-2026-0714-compressed.pdf) (2026-07-14)
- [Nielsen Q1 2026 Ad Supported Gauge](https://www.nielsen.com/news-center/2026/nielsens-q1-2026-ad-supported-gauge/) (2026)
- [MovieLabs: The 10 principles of the 2030 Vision](https://movielabs.com/the-10-principles-of-the-2030-vision/) (2019)

---

# The pack (written 2026-10-28)

One guest article for StreamingMeme's Industry Voices, under Arash's byline: the encoding industry's per-title lesson applied to everything after delivery.

## Streaming's next per-title moment won't happen in the encoder

_per-scene-01 · StreamingMeme Industry Voices, after Arash approves · Guest article (StreamingMeme) · Industry Trend Commentary_

*Ten years ago the encoder learned to read the content. Ad breaks, artwork, previews and discovery still treat every minute the same.*

Ten years ago streaming learned that the content should decide how it gets treated. We applied that lesson to bits and to very little else.

In December 2015, Netflix described per-title encoding on its engineering blog. Until then every title got the same bitrate ladder, topping out at 5,800 kbps for 1080p, whatever was in the picture. A cartoon and an action film were encoded as if they were equally hard to compress.

Per-title gave each title "a unique bitrate ladder, tailored to its specific complexity characteristics", and Netflix told reporters the change would cut bandwidth by about 20%.

The idea then moved down to smaller units. Netflix demonstrated shot-based encoding in 2017 and wrote up its Dynamic Optimizer in 2018, choosing resolution and quality shot by shot to score as high as possible on VMAF, its perceptual quality metric.

When it moved 4K to optimized shot-based encoding in 2020, it reported about half the bitrate for the same quality and expected more than 65% fewer rebuffers per hour.

The rest of the industry followed quickly. AWS added quality-defined variable bitrate to MediaConvert in August 2018 and automated per-title ladders in the same product in 2020, so a team could switch it on instead of building it.

I think the reason it spread so fast matters more than the encoding itself, because that's the part we haven't copied yet.

## Why per-title worked

Per-title encoding succeeded because four things lined up:

- The analysis happened once, when the title came in.
- The result was stored as data (the ladder) and travelled with the asset in the manifest.
- Every player used it automatically, without anyone deciding title by title.
- There was a metric people trusted. Netflix open-sourced VMAF in June 2016, and arguments about picture quality turned into arguments about numbers.

Everything after delivery is missing at least one of those four, and usually all of them.

## The fixed ladder is still everywhere else

Look at what happens to a title once it's encoded. Most of the decisions are still made the way we encoded video before 2015, with one rule for everything.

Ad breaks are placed on a timer, by a rule that looks for black frames and silence, or by an editor scrubbing through the timeline. In the workflow we've shown with SDVI, a single 40-minute episode can take 20 to 60 minutes to segment by hand.

That number grows with the ad business. Streaming reached 46.6% of ad-supported TV viewing in Nielsen's Q1 2026 Gauge, and Ampere data reported by Business Insider puts the average ad load across the big US services up about 18% between January and August, so the hours of manual work grow with every title that moves into an ad tier.

Artwork is often a frame grab or a quick manual pick, even though it may be the most important image on the service.

Netflix's research from early 2014 found that artwork was the biggest influence on what members chose and took "over 82% of their focus while browsing". Netflix also saw members spend about 1.8 seconds considering each title.

A single one-hour episode of Stranger Things contains nearly 86,000 still frames, which is why Netflix built tooling to rank them for its editors. On a service without that tooling, those 1.8 seconds go to whichever frame someone happened to grab.

Previews and clips need someone to find the moment worth showing. When that someone is an editor working title by title, the long tail of the catalogue rarely gets one.

Discovery leans on genre tags and viewing history. Netflix's own researchers wrote in 2015 that a typical member loses interest after perhaps 60 to 90 seconds of choosing, having reviewed 10 to 20 titles.

Tags decay as well. When we rebuilt the vocabularies in Fingerprint+, our metadata product, this autumn we removed 833 terms. Labels like "calm" and "calming" had split one idea in two, so every filter built on one of them saw only part of the titles.

The cost of all this lands on the library. Luminate's midyear report counts 42.2 billion hours of library TV streamed in the US in the first half of 2026, against 11.5 billion for original series, and library film added another 10.8 billion hours.

By my count that makes library almost four in five hours of TV streaming. I'd expect them to be the titles least likely to get hand-picked artwork, a hand-cut preview or carefully placed breaks.

![Two pipelines. Today: ingest, then content-aware encoding, then package and deliver, after which ad breaks, artwork, previews and discovery all run on content-blind defaults. Next: ingest, then a scene-level content layer computed once, which feeds encoding, ad markers, artwork, clips and previews, and discovery.](figures/per-scene-01-pipeline.png)

## What a scene-level content layer contains

The equivalent of the bitrate ladder for everything after delivery is a scene-level description of the title, computed once at ingest and stored next to the mezzanine file. At Vionlabs this is what we build. In practice it holds:

- Scene and shot boundaries, and how similar each shot is to the ones around it
- Where people speak, where it goes quiet and where the picture goes to black
- Intros, recaps and end credits
- An emotion and tension curve across the runtime, showing where the story builds and where it rests
- Break candidates, each rated by how many of those signals agree on the spot
- Key moments: the frames and short ranges most likely to work as artwork, previews or clips
- An embedding of each title's visual composition, pacing, dialogue, tone and emotional arc, so systems can compare how titles feel to watch instead of which genre label they share

Most of that isn't new. Plenty of media teams already have a script for black frames or a spreadsheet of credit timestamps. What changes is producing it once, in one schema, so that ad decisioning, artwork tools and recommenders all read the same answer.

That's also where the industry's own plans point. In 2019 the major studios, through MovieLabs, set out ten principles for how media will be made by 2030.

The first says assets are "created or ingested straight into the cloud and do not need to be moved". The second says "applications come to the media".

A content layer applies the same principle to understanding. Analyse the file where it lives, once, and let every system that needs to know what's in it come to the result.

## Where it sits in the pipeline

The layer belongs at ingest, next to the encode job, run by whatever orchestrates the media supply chain.

Our ad-break work with SDVI is a public example. Content lands in SDVI's Rally platform, which routes it to our analysis without a manual handoff. Ranked break candidates come back in minutes.

An operator then reviews them on a frame-accurate timeline in Codemill's validation tool and approves or adjusts each one. The final markers go downstream as SCTE markers or sidecar files to ad insertion.

That last step shows where the understanding currently stops. SCTE-35 can say a good deal about a point in time: a time_signal with a segmentation descriptor can mark a chapter start or a provider placement opportunity.

VMAP gives each break a time offset, and OpenRTB 2.6 can say whether an ad pod is the first or the last in the programme.

None of them scores how good a break point is or where it falls in the story, and I couldn't find a field for that in any of the ad standards I checked.

So the scene layer knows a break sits at a natural pause after a resolved scene, while the bid request downstream only knows a timestamp.

I think break quality should travel with the cue, the same way the bitrate ladder travels in the manifest. **Publishers would then have a way to prove a break respects the story, and buyers would have a reason to pay for it.**

## What changes for each team

For ad operations, break placement becomes a review job. The team checks ranked candidates instead of scrubbing through every title, and the work grows with the number of titles to review rather than with the hours of video.

For editorial and marketing, artwork and previews start from moments the layer has already found. An editor chooses between strong options instead of hunting through tens of thousands of frames.

For product and discovery, rows and recommendations can use how a title feels to watch. That helps most with new and long-tail titles, which have little viewing history to learn from.

For engineering, it is one more job at ingest with a versioned output. I would run it the way teams run the encoding ladder, with a schema, a version number and a test before a new model goes live.

## What we got wrong on the way

Models make confident mistakes. In the SDVI webinar this summer I described one: a camera panning across a wall into darkness can look like a black frame to the model, so it gets flagged as a break. That's why the operator stays in the workflow.

A rested, focused editor still makes very good calls. The model wins on speed and consistency across thousands of titles, and the two together beat either one alone.

Vocabularies rot if nobody owns them. Every new tag looks like extra coverage until two tags mean the same thing.

Our genre list had grown to 152 terms, including compound labels such as "action comedy" that forced a choice nobody downstream could see. The fix was to treat the vocabulary as a product with a schema and versions, and to cut hard.

General-purpose video models see more than they understand. Recognising objects, faces and speech is largely solved.

Telling whether tension is building or releasing, or whether a scene is the end of a marriage or the start of a romance, is a different problem. It's the one that matters most for ads, artwork and discovery, and it needs models trained on entertainment.

## The case against

The strongest objection comes from recommendation research. In 2009, Pilászy and Tikk showed on Netflix Prize data that even ten ratings of a new film were worth more for predicting what users would think of it than all its metadata. Where you have viewing history, collaborative filtering is hard to beat.

I agree, and it tells you where content signals earn their place. They matter most where history is thin: new titles, the long tail and the library titles nobody has opened in years.

That's the case Curio, our personalization layer, was built for. It runs on embeddings learned from more than a million analysed assets, and Great American Pure Flix became its first partner in October.

Ad breaks and artwork aren't recommendation problems at all. A film with a million views still needs its breaks placed and its artwork chosen, and its viewing history says nothing about where the story pauses.

The second objection is accuracy. On the Video-MME benchmark published in 2024, the best commercial model at the time answered about 75% of questions about videos correctly, and it did worse on longer videos.

A content layer will be wrong some of the time. That's an argument for review where judgment matters and for measuring everything, which is how encoding got there too.

## Where I'd start

If you run a streaming service, the encoding history suggests starting where there's a number. Pick one use case, measure it before and after, and let the result decide whether you do the next one:

- Time to segment a title for ads, by hand against reviewed AI markers
- Drop-off in the 30 seconds after a break, split by whether it landed at a natural pause or mid-scene
- Click-through on artwork chosen from key moments, against the frame grab it replaces
- How many library titles get started each week once they have a real preview and real artwork

Per-title spread once VMAF gave everyone the same number to argue about. I think content understanding needs its own version of that: an agreed way to score a break, a thumbnail or a preview, so that a platform can compare one approach with another.

What would you need to see measured before you trusted a scene-level layer to place your breaks or pick your artwork?

*Arash Pendari is the founder and CEO of Vionlabs, which builds AI that understands how video content feels to watch, for streaming services, broadcasters and telcos. [vionlabs.com](https://www.vionlabs.com)*

**Sources:** [Netflix per-title encoding (The Register)](https://www.theregister.com/2015/12/16/netflix_per_title_encode_optimization/) (2015-12-16); [Netflix 4K optimized shot-based encoding (Hackaday)](https://hackaday.com/2020/09/16/decoding-the-netflix-announcement-explaining-optimized-shot-based-encoding-for-4k) (2020-09-16); [AWS MediaConvert adds QVBR](https://aws.amazon.com/about-aws/whats-new/2018/08/aws-elemental-mediaconvert-now-supports-quality-defined-variable-bitrate-qvbr-encoding) (2018-08); [Netflix: The Power of a Picture](https://about.netflix.com/en/news/the-power-of-a-picture) (2016-05-03); [Netflix: AVA, the art and science of image discovery](https://medium.com/netflix-techblog/ava-the-art-and-science-of-image-discovery-at-netflix-a442f163af6) (2018); [Gomez-Uribe and Hunt, The Netflix Recommender System (ACM TMIS)](https://gwern.net/doc/reinforcement-learning/exploration/2015-gomezuribe.pdf) (2015-12); [Luminate 2026 Midyear Report](https://luminatedata.com/wp-content/uploads/2026/07/Midyear-REPORT-2026-0714-compressed.pdf) (2026-07-14); [Nielsen Q1 2026 Ad Supported Gauge](https://www.nielsen.com/news-center/2026/nielsens-q1-2026-ad-supported-gauge/) (2026); [MovieLabs 2030 Vision principles](https://movielabs.com/the-10-principles-of-the-2030-vision/) (2019); [AWS MediaTailor: SCTE-35 messages](https://docs.aws.amazon.com/mediatailor/latest/ug/ca-scte-35-messages.html) (current docs); [IAB VMAP](https://iab.com/vmap) (2014); [Pilászy and Tikk, RecSys 2009](https://bibtex.github.io/RecSys-2009-PilaszyT.html) (2009); [Video-MME benchmark](https://arxiv.org/pdf/2405.21075) (2024-05); [Vionlabs and SDVI ad-break webinar](https://www.vionlabs.com/news/accelerating-ad-breaks-detection-and-insertion-webinar-with-sdvi) (2026-08-19); [Vionlabs: What's new in Fingerprint+ v11.15](https://www.vionlabs.com/news/whats-new-in-fingerprint-v11-15) (2026-10-09); [Vionlabs launches Curio with Great American Pure Flix](https://www.vionlabs.com/news/vionlabs-launches-curio) (2026-10-01); [Ampere ad load data (Android Authority)](https://www.androidauthority.com/streaming-services-more-ads-2026-3708866/) (2026-09); [AWS MediaConvert automated ABR](https://aws.amazon.com/about-aws/whats-new/2020/11/automated-abr-configuration-now-available-in-aws-elemental-mediaconvert) (2020-11); [OpenRTB 2.6 and AdCOM 1.0 (IAB Tech Lab)](https://github.com/InteractiveAdvertisingBureau/openrtb2.x) (2.6)

## Fact-check before posting

| Claim | Source | Status |
| --- | --- | --- |
| Netflix per-title encoding post, 14 Dec 2015; one fixed ladder topping out at 5,800 kbps; 'tailored to its specific complexity characteristics' | [StreamingMedia; The Register](https://www.theregister.com/2015/12/16/netflix_per_title_encode_optimization/) 2015-12 | confirmed |
| About 20% less bandwidth, from Netflix's statements to the press | [Fortune; Tubefilter](https://fortune.com/2015/12/15/netflix-less-data) 2015-12-15 | confirmed |
| Shot-based encoding demonstrated at MWC 2017; Dynamic Optimizer written up in 2018, maximising VMAF per shot | [Quartz; arXiv 1808.03898](https://arxiv.org/pdf/1808.03898) 2017-2018 | check |
| 4K optimized shot-based encoding (2020): about 50% bitrate saving; over 65% fewer rebuffers per hour expected | [TV Technology; Hackaday; TVBEurope](https://hackaday.com/2020/09/16/decoding-the-netflix-announcement-explaining-optimized-shot-based-encoding-for-4k) 2020 | confirmed |
| VMAF open-sourced June 2016 | [Netflix TechBlog via Wikipedia; Streaming Learning Center](https://github.com/Netflix/vmaf) 2016-06 | confirmed |
| AWS MediaConvert QVBR (Aug 2018) and automated ABR per-title ladders (Nov 2020) | [AWS What's New](https://aws.amazon.com/about-aws/whats-new/2020/11/automated-abr-configuration-now-available-in-aws-elemental-mediaconvert) 2018 / 2020 | confirmed |
| Artwork 'the biggest influencer' and 'over 82% of their focus while browsing' (2014 research); about 1.8 seconds per title | [Netflix, The Power of a Picture; Engadget](https://about.netflix.com/en/news/the-power-of-a-picture) 2016-05-03 | confirmed |
| A one-hour Stranger Things episode has nearly 86,000 static video frames | [Netflix TechBlog (AVA)](https://medium.com/netflix-techblog/ava-the-art-and-science-of-image-discovery-at-netflix-a442f163af6) 2018 | confirmed |
| A member loses interest after perhaps 60 to 90 seconds, having reviewed 10 to 20 titles | [Gomez-Uribe and Hunt, ACM TMIS](https://gwern.net/doc/reinforcement-learning/exploration/2015-gomezuribe.pdf) 2015-12 | confirmed |
| Luminate H1 2026: library TV 42.2bn hours vs 11.5bn original TV; library film 10.8bn | [AP (syndicated); Soundstock](https://luminatedata.com/wp-content/uploads/2026/07/Midyear-REPORT-2026-0714-compressed.pdf) 2026-07-15 | confirmed |
| Streaming 46.6% of ad-supported TV viewing, Q1 2026 | [Nielsen; TV Technology](https://www.nielsen.com/news-center/2026/nielsens-q1-2026-ad-supported-gauge/) 2026 | confirmed |
| MovieLabs 2030 Vision principles 1 and 2 (assets ingested straight into the cloud; applications come to the media) | [MovieLabs release 20 Aug 2019; Advanced Television](https://movielabs.com/the-10-principles-of-the-2030-vision/) 2019-08-20 | confirmed |
| SCTE-35 time_signal and segmentation descriptors (chapter, provider placement opportunity); VMAP timeOffset; OpenRTB 2.6 podseq first/last; no field scoring break quality or story position | [Comcast scte35-go; IAB VMAP; OpenRTB 2.6 and AdCOM 1.0](https://github.com/InteractiveAdvertisingBureau/openrtb2.x) current | confirmed |
| Pilászy and Tikk 2009: even 10 ratings of a new movie are more valuable than its metadata | [RecSys '09 abstract; arXiv 1711.10816](https://bibtex.github.io/RecSys-2009-PilaszyT.html) 2009 | confirmed |
| Video-MME (2024): Gemini 1.5 Pro about 75%, accuracy declines on longer videos | [arXiv 2405.21075; Video-MME README](https://arxiv.org/pdf/2405.21075) 2024-06 | confirmed |
| Ampere: ad minutes per hour up about 18% Jan to Aug 2026 (exclusive to Business Insider) | [Android Authority; MediaPost](https://www.androidauthority.com/streaming-services-more-ads-2026-3708866/) 2026-09 | check |
| SDVI workflow: 40-minute episode takes 20 to 60 minutes to segment by hand; Rally, validation, SCTE or sidecar delivery; pan-into-darkness example | [Vionlabs webinar page](https://www.vionlabs.com/news/accelerating-ad-breaks-detection-and-insertion-webinar-with-sdvi) 2026-08-19 | confirmed |
| Fingerprint+ v11.15 removed 833 terms; genre list had 152 terms | [Vionlabs release notes](https://www.vionlabs.com/news/whats-new-in-fingerprint-v11-15) 2026-10-09 | confirmed |
| Curio runs on embeddings learned from more than 1,000,000 analysed assets; Great American Pure Flix first partner | [Vionlabs release](https://www.vionlabs.com/news/vionlabs-launches-curio) 2026-10-01 | confirmed |

## How this was made

- Two research agents (encoding and artwork history; pipeline standards and market data) and one verification agent, 28 Oct 2026. Primary sites (Netflix, MovieLabs, StreamingMeme) were blocked by the session's network, so facts were confirmed across search results and secondary reports.
