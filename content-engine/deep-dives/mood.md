# What a machine means by mood

_Technology explained · for Product and metadata leads, Tier-1 streamers, Telco / cable operators, Buyers comparing vendors_

**Mood is on every metadata spec sheet now, and the word covers very different things. A tag on a title guessed from its synopsis is not emotion read from picture and sound, scene by scene, and checked against how people watch. Buyers deserve a way to tell them apart.**

## Why now

ThinkAnalytics, ContentWise, Bitmovin, PA TV Metadata and Eon Media all sell mood or emotion attributes in 2026. A spec sheet can't show the difference. Generic language models also invent metadata: in Gracenote's own test an ungrounded model made up every attribute for 506 of 2,600 titles.

## Questions the series answers

- Where does the signal come from: synopsis and subtitles, or picture and sound?
- One tag per title, or a curve across the runtime, and why does it matter?
- How do you check a model's read of emotion when there is no single right answer?
- What does the emotion curve of a well-known film look like next to its plot points?
- Five questions any buyer can ask a vendor in the first meeting

## What Vionlabs brings

Fingerprint+ emotion-aware embeddings and Metadata Enrichment; scene-level emotion curves; the Fingerprint Plus 11.15 release (cleaner vocabularies, Arabic, better synopses); the existing post 'Your AI Can See the Scene. It Can't Feel It.'

## Get before publishing

- An emotion curve for one well-known title we are allowed to show
- A plain-language note from the data team on how the model is validated
- A decision on how much of the method we describe in public

## Events

- Satis, Paris (4–5 Nov), on the Embrace booth

## Series plan

1. **Five things 'mood' can mean on a metadata spec sheet** (Blog post (vionlabs.com), Product & AI Insight)
2. **One film, two timelines: what happens vs how it feels** (Carousel, Product & AI Insight)
3. **A synopsis is marketing copy. Don't build your metadata on it.** (Text, Opinion / Contrarian Take)
4. **How do you check a machine's feelings?** (Text, Product & AI Insight)
5. **The people who taught our models what tension looks like** (Image + text, Behind the Scenes)

## Evidence

- [ThinkAnalytics ContentDNA (40K+ attributes incl. mood)](https://thinkanalytics.com/think-metadata/) (2026)
- [ContentWise Open Enricher](https://contentwise.com/open-enricher/) (2026)
- [Nine deploys Bitmovin AI Scene Analysis](https://www.broadbandtvnews.com/2026/09/11/nine-deploys-bitmovin-ai-scene-analysis-for-vod-workflows/) (2026-09-11)
- [PA TV Metadata EMMET enrichment tool](https://www.tvbeurope.com/media-consumption/pa-tv-metadata-aims-to-improve-content-discovery-with-ai-supported-enrichment-tool) (2026-04)
- [Gracenote adds sports MCP server, entertainment SLM and agents (506 of 2,600 titles)](https://ppc.land/gracenote-adds-sports-mcp-server-entertainment-slm-and-agents-to-ai-roadmap/) (2026-09-09)

## From the Content Radar

- 2026-W43 gap: Emotion across the runtime
- 2026-W43 theme: Metadata enrichment is what personalisation runs on
- Ideas 2026-W43-06 and -08

---

# The pack (written 2026-11-11)

The W46 long read for the Wednesday draft to Arash: mood-first discovery, hooked on Netflix's AI Discover test (3 Nov) and timed before the DPP Leaders' Briefing. The carousel and posts are still to write.

## Mood-first discovery needs a different scene for every mood

_mood-01 · On vionlabs.com when Arash approves · Blog post (vionlabs.com) · Product & AI Insight_

*Netflix now asks viewers how they want to feel before it shows a title. Most titles fit several moods, and each one needs its own way in.*

When a viewer tells you how they want to feel, the scene you show them matters more than the title you pick.

Netflix made that concrete last week. On 3 November it began [testing AI Discover](https://about.netflix.com/news/introducing-ai-discover), a new tab on its TV app for a small group of US members. Instead of rows of titles, it opens with themes such as "Something Light", "Scare Me", "Family Movie Night" and "Quick Watches", each previewed with a clip from a show or movie. Choosing one brings up matching recommendations, and narrower themes follow until something feels right.

Netflix calls it a test kitchen, and it isn't alone. Disney+ has been testing AI search with a small group of subscribers since August, and EE launched a Mood Matcher on its TV service in the spring.

I think this is the right direction, and it creates a problem most catalogues aren't ready for.

## One title, several moods

Most titles fit more than one mood. A tight 95-minute thriller belongs under "Scare Me". It also belongs under "Quick Watches", and possibly under "Something Different" for a viewer who has only watched comedies this month.

The clip that sells it in one place can be wrong in another. For "Scare Me" you want the moment the lights go out in the house. For "Quick Watches" you want the opening two minutes that show how fast the story moves. A viewer who picked "Something Light" and gets the scariest scene in the film backs out, and they probably don't come back to that title.

A mood-first screen multiplies the number of contexts each title appears in, and each context needs its own way in.

## Netflix already knows the picture decides

None of this is new to Netflix. Its own research from early 2014 found that artwork made up more than 82% of members' focus while browsing, at an average of 1.8 seconds per title.

In 2017 Netflix [described how it personalises artwork](https://netflixtechblog.com/artwork-personalization-c589f074ad76): a member who watches romance might see Good Will Hunting represented by Matt Damon and Minnie Driver, while a comedy fan sees Robin Williams. Its engineers wrote that looking at each image in isolation isn't enough, because what matters is the set of images a member sees across a page and a session.

AI Discover extends the same logic from artwork to clips, and from viewing history to the mood a viewer chooses in the moment. The question every service now has to answer is which scene, for which mood, in which title.

## Knowing how each scene feels

Answering that takes more than a mood tag on the title. A tag guessed from the synopsis can tell you a film is a thriller. It can't tell you where the tension peaks, which scene is the funny one, or where the story pauses long enough for a clean ten-second clip.

That needs a description of every scene: the emotion, the pacing, who is on screen and where the moment begins and ends. At Vionlabs this is what we build, and in June I wrote about the same idea for thumbnails under the heading ["same title, different emotional entry point"](https://www.vionlabs.com/news/your-thumbnails-are-broken-at-scale-story-aware-ai-built-for-entertainment-fixes-it). A viewer drawn to thrillers should see the tension frame. A viewer drawn to romance should see the frame with the emotional connection.

We've learned two things doing this. Preview clips often start at the beginning of an episode even when the emotional payoff comes ten minutes later, so the default clip is usually the weakest one. And editors make the best final call when they choose between strong candidates instead of hunting through the whole film, which is why our tools hand them ranked moments to approve rather than replacing them.

The data behind it also has to be consistent. When Plex added our mood data across a catalogue gathered from many distributors and decades, its A/B testing showed a clear uplift in viewing minutes.

## What the content owner still controls

On Netflix, Netflix chooses the clip. Every other service building mood-first screens will need the same raw material, though: a scene-level description of each title it can map to its own moods.

For broadcasters and studios whose catalogues sit on several platforms, that description is something they can own and deliver with every title, the same way they deliver artwork and subtitles. I think it will decide which titles get picked for "Scare Me" and which never appear there at all.

## The case against

Mood is fickle, and that is the strongest objection. Disney's own example is someone who usually watches crime dramas but is suddenly in the mood for something lighter, so the viewer has to state the mood each time, and many won't bother. I haven't found a published study showing that mood-first discovery beats recommendations based on viewing history.

Netflix is hedging too. It calls AI Discover a test, keeps its normal home screen, and gives every title a "Tune Your Recommendations" button. In 2020 it also let members switch off autoplay previews after complaints.

I agree with all of that. Choosing a mood only narrows the list, and what persuades a viewer to press play is still the image or clip they see for that title. Previews annoy people when they show the wrong moment at the wrong time, and the answer to that is a better-chosen scene rather than no preview at all.

## Where I'd start

If you run a streaming service or deliver a catalogue to one, these tests are cheap:

- For your 50 most-watched titles, list every mood each one could fit, and count how many have more than one preview clip
- Test a mood-matched clip against the standard trailer in a single rail, and measure click-to-play
- Check how many of your preview clips start in the first minute of the title, regardless of where the strongest moment is
- Track how often viewers back out of a title after its preview plays

We'll be at the DPP Leaders' Briefing in London next week. If your catalogue had to answer "Scare Me" tomorrow, which scene would you show?

*Want to see which scenes in your catalogue fit which mood?*

[**Book a demo with Vionlabs →**](https://www.vionlabs.com/book-a-demo)

**Sources:** [Introducing AI Discover (Netflix)](https://about.netflix.com/news/introducing-ai-discover) (2026-11-03); [Netflix's new AI Discover tab helps you find something to watch based on your mood (TechCrunch)](https://techcrunch.com/2026/11/03/netflixs-new-ai-discover-tab-helps-you-find-something-to-watch-based-on-your-mood/) (2026-11-03); [AI-powered search for ESPN and Disney+ (The Walt Disney Company)](https://thewaltdisneycompany.com/news/ai-powered-search-espn-disney-plus/) (2026-08-06); [EE TV introduces conversational AI-powered search (EE newsroom)](https://newsroom.ee.co.uk/ee-tv-transforms-the-tv-experience-by-becoming-the-uks-first-pay-tv-service-to-introduce-conversational-ai-powered-search/) (2026-03-31); [The Power of a Picture (Netflix)](https://about.netflix.com/news/the-power-of-a-picture) (2016-05-03); [Artwork Personalization at Netflix (Netflix Tech Blog)](https://netflixtechblog.com/artwork-personalization-c589f074ad76) (2017-12-07); [Your Thumbnails Are Broken at Scale (Vionlabs)](https://www.vionlabs.com/news/your-thumbnails-are-broken-at-scale-story-aware-ai-built-for-entertainment-fixes-it) (2026-06-10); [Boosting viewer engagement with AI: thumbnails and preview clips (Vionlabs)](https://www.vionlabs.com/news/boosting-viewer-engagement-with-ai-revolutionizing-thumbnails-and-preview-clips) (2025-05-12); [Plex customer story (Vionlabs)](https://www.vionlabs.com/customer-stories/plex) (2026-05-05); [Netflix lets you turn off autoplay previews (Engadget)](https://www.engadget.com/2020-02-06-netflix-autoplay-preview-settings.html) (2020-02-06)

## Fact-check before posting

| Claim | Source | Status |
| --- | --- | --- |

## How this was made

- Two research agents (Netflix AI Discover and mood-first launches; Vionlabs' public proof) and one verification agent, 11 Nov 2026. Firecrawl credits ran out mid-research, so the last checks used web search snippets.
