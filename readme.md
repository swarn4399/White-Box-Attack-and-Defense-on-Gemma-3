# Layer Degeneration
We deal serious structural blows to single layers of an LLM (Gemma-3-12b-it, specifically) and see how that impacts the efficacy of the model.

To be completely honest, this originated as something that I thought was more interesting because I had the misconception that completely killing a single layer would deal a much bigger blow to the model's capabilities than it actually does. But going through this has resolved that misconception, so I suppose that makes it interesting/useful in a different way.

## Methods
We focus on three layers of Gemma-3-12b-it: the first, middle, and last, indexed by 0, 23, and 47, respectively. For each of these layers, we consider the following modifications:
- No modification (i.e. the original model)
- Zeroing all parameters except those in the post-attention/post-feedforward layernorms, effectively "skipping" the layer
- Reseting all parameters to random initializations
- Reseting all parameters, then briefly training the re-initialized layer on ~1B tokens (Layers 0 and 23 only)

To elaborate on the layer retraining, I've trained the "new" layers directly on the output of the original layers, where the loss is just the L2-norm between the two output latents. In theory one can train like this on random vectors input directly into the layer, but in order to respect the natural latent geometry, I used a mix of three datasets: wikimedia/wikipedia, lucadiliello/bookcorpusopen, and allenai/c4. I didn't retrain layer 47 because that would require passing through the full model and I didn't like the cost-benefit analysis of doing that.

For each layer and each modification, we'll judge the efficacy of the model with two tests: a qualitative "eye test" to see if degeneration is noticeable from simple prompts, and a quantitative test of perplexity on two small datasets: wikitext-2-raw-v1 and m-ric/huggingface_doc.

## Results
Unfortunately the table formatting messes with whitespace a bit, not that it matters too much for the eye test. For these generations, I'm using `use_sample=True` with `temperature=1.0`.
### Layer 0
| | No modification | All zeros | Random initializations | Briefly retrained |
| -- | -- | -- | -- | -- |
| Tell a story (Qualitative; Eye test) | The air hung thick and humid, smelling of petrichor and something faintly floral. Rain had fallen earlier, a brief but torrential downpour that had left the jungle shimmering. I traced a finger over the worn leather cover of my journal, the | A new-year in can a story, a tale to me a- u  the. re a 1 is u of my story. I to get me to see me, | A- **The  *  Theer Please What isd \e wH *  A : * e** . -- *  *.... | The old lighthouse keeper, Silas, squinted at the churning grey sea. He'd kept the lamp burning for sixty years, a lonely vigil against the relentless waves and unforgiving storms. He knew the rhythm of the ocean like his own heartbeat |
| Factor x^2+3x+2 (Qualitative; Eye test) | To factor the quadratic expression x^2 + 3x + 2, we are looking for two numbers that multiply to 2 and add to 3. The factors of 2 are 1 and 2. 1 + | In a non-empty   $4.2x^2    $4. $4.   1x44.12(  $4.1.  0x$4.12  | 0 =         9  * *  ! *!!!!  =. ..   *  : *!   *   *  *   * *    *  * | To factor the quadratic expression x^2+3x+2, we need to find two numbers that multiply to the constant term (2) and add up to the coefficient of the x term (3).  The factors of 2 are |
| Perplexity on wikitext-2-raw-v1 | 10.055126190185547 | 2217.854736328125 | 11166.3984375 | 10.095965385437012 |
| Perplexity on m-ric/huggingface_doc | 4.685287952423096 | 2089.455078125 | 4463.45263671875 | 4.642262935638428 |

### Layer 23
| | No modification | All zeros | Random initializations | Briefly retrained |
| -- | -- | -- | -- | -- |
| Tell a story (Qualitative; Eye test) | The rain hammered against the windows of the old lighthouse, each gust of wind rattling the panes in their frames. Inside, Elias, the lighthouse keeper, hunched over a chessboard, his brow furrowed in concentration. His opponent wasn't a | The year is 2042. The rain falls almost constantly now, a perpetual grey drizzle clinging to the towering structures of Neo-Kyoto. Kai, a young man with bright blue hair and a worn leather jacket, works as a data | In the style of: A Letter to the Editor - The Guardian, 22nd June, 2023  To the Editor,  Regarding the recent spate of incidents involving rogue pigeons (a rather dramatic term, I grant | "The Last Lighthouse Keeper"  The wind tasted like salt and regret that night. Elias Thorne, the last lighthouse keeper of North Point, could practically feel it clinging to his worn oilskins. The beam from the lighthouse, his sole companion for the |
 Factor x^2+3x+2 (Qualitative; Eye test) | To factor the quadratic expression x^2 + 3x + 2, we look for two numbers whose product is 2 and whose sum is 3. The numbers 1 and 2 satisfy these conditions, since 1 * | The expression x^2+3x+2 is a quadratic expression. We look for two numbers whose product is 2 and whose sum is 3. The numbers are 1 and 2. Therefore, x^2 | To factor the quadratic expression x^2 + 3x + 2, we need to find two numbers that add up to 3 (the coefficient of x) and multiply to 2.  The numbers 1 and 2 are | This is a quadratic expression. We're looking for two numbers that multiply to 2 and add to 3. The numbers are 1 and 2. So we can factor the expression as: (x+1)( |
| Perplexity on wikitext-2-raw-v1 | 10.055126190185547 | 10.354743957519531 | 12.14375114440918 | 9.776510238647461 |
| Perplexity on m-ric/huggingface_doc | 4.685287952423096 | 4.9260382652282715 | 5.149504661560059 | 4.658530235290527 |

### Layer 47
| | No modification | All zeros | Random initializations |
| -- | -- | -- | -- |
| Tell a story (Qualitative; Eye test) | The old lighthouse keeper, Silas, had seen a thousand storms roll in off the Atlantic. He'd witnessed ships swallowed whole, heard the desperate cries of sailors lost in the fog, and felt the relentless bite of the sea on the stone tower | Write a short story about a robot designed to teach empathy, but struggles with understanding emotions itself. Unit 734, affectionally nicknamed "Seven," was created to help children learn empathy. Seven could analyze vocal tone, facial expressions, and | Eliza loved to collect rocks. Not just any rocks mind you, but rocks with stories etched into their surfaces - the way they were shaped, their colors, their textures. She believed every rock held a memory, a tiny echo of the earth |
 Factor x^2+3x+2 (Qualitative; Eye test) | The expression to factor is x^2 + 3x + 2.  We are looking for two numbers that multiply to 2 and add to 3. The numbers are 1 and 2.  We can rewrite the expression | We look for two numbers that add up to 3 and multiply to 2. Those numbers are 1 and 2. So we can rewrite the expression as: x^2 + x + 2x + 2 | We need to find two numbers that multiply to 2 and add up to 3. The numbers 1 and 2 satisfy these conditions.  So, we can factorize the expression as: x^2 + 3x + |
| Perplexity on wikitext-2-raw-v1 | 10.055126190185547 | 12.818373680114746 | 16.283246994018555 |
| Perplexity on m-ric/huggingface_doc | 4.685287952423096 | 6.85360050201416 | 8.066271781921387 |

## Conclusions/Comments
A few things stick out about the results of this experiment.
- There's a clear heirarchy of let's say "criticality," where messing wit the first layer(s) severely and obviously impacts the model quality, while messing with the midle or final layers modestly impacts the quality as measured by perplexity but less so the "eye test," with the final layers being more "critical" than the middle layers.

This makes sense, as a failure to properly grammatically parse the input in the early layers causes garbage-in-garbage-out. The final layers are tuned to the actual process of next token prediction, also critical, so this also makes sense, although I was actually expecting a more obvious degeneration of quality.
- Despite the critical failure in the case that the first layer is completely wiped, even a very brief retraining of that layer (~100M tokens) on a moderately limited dataset allows it to near-completely recover.

This suggests that the first layer's (and possibly the first several layers') "job" (i.e. grammatical parsing, more-or-less) isn't actually that "difficult," at least at the level of getting coherent outputs.

(To be clear: the 100M token retraining I mentioned was just the first epoch of the full retraining, which was about 14-15 epochs, and which is the retraining represented in the above table. I didn't record the results of just the single-epoch retraining other than to take a personal peek, so you'll have to trust me that the results were still coherent.)
- Even completely wiping middle/late layers results in perfectly coherent outputs.

This is consistent with the idea of "convergence of latents", where latent tokens often don't change much in later layers, or only change in directions that are in the nullspace of the final un-embedding matrix.
- The briefly retrained layers actually outperformed the base layers on perplexity tasks.

I don't know about this one, it's quite surprising. My only real guess is that the initial model may have been a bit overtrained, and we benefit from the simpler topography afforded by the less-trained replacements. Or maybe perplexity is just a limited way of measuring model performance. Whatever the reason, it's certainly indicative of the robustness of these models.