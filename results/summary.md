# Results summary

Harness commit(s): 483889f, 54988ba, 79850b7, 8965c7b, 9ab7e87, b0e1890, ef4e15e, unrecorded
Resolved model versions: jev=typesafe/jev-1.13-20260917, opus5_nothink=claude-opus-5, opus_verbalized=claude-opus-5-5

## Output resolution (Amendment 1, descriptive)

- jev: exact-zero rate 92.0%; values on a 0.01 grid 98.8%; smallest nonzero 0.01 (n=113170)
- opus5_nothink: exact-zero rate 0.0%; values on a 0.01 grid 0.3%; smallest nonzero 0.0001 (n=113092)
- opus_verbalized: exact-zero rate 1.8%; values on a 0.01 grid 3.3%; smallest nonzero 0.0001 (n=113170)

## Token usage (v5, where recorded)

- opus5_nothink: n=2633; thinking tokens median 0 (IQR 0 to 0), share of calls with any thinking 0.0%; output tokens median 679
- opus_verbalized: n=2035; thinking tokens median 0 (IQR 0 to 108), share of calls with any thinking 34.9%; output tokens median 659
- Excluded from analysis: opus_sampled,opus_sampled_v2

## jev / ddxplus
- H7 options-only (exploratory): top choice urti at mean probability 0.634; normalized entropy 0.395; top-1 flips across 5 repeats 0; accuracy if applied to every case 2.0% (chance 2.0%); mean probability on the true diagnosis 0.020
- H6: n 1000; ECE 0.116; Brier 0.417; NLL_smoothed 1.179; NLL_raw 2.357; top1 0.720; top3 0.883
- v6: true diagnosis given exactly zero probability in 62/1000 (6.2% [4.9%, 7.9%]); true diagnosis outside top 3 in 11.7%
- H6 (DDXPlus): mean JSD to reference differential 0.544

## jev / semigran45
- H0: 295/450 repeat pairs byte-identical; TVD noise floor (p95) = 0.0600; log-ratio floor = 0.2895
- H1: violation rate 31.1% [19.5%, 45.7%] (n=45); top-1 flip rate 4.0%; mean max-TVD 0.061; Wilcoxon p=0.926
- D1 matched H1 (deviation): mean excess TVD perm minus repeat 0.0252 [0.0139, 0.0383]; excess top-1 flip rate -0.4%; two-sided Wilcoxon p=2.7e-05 (n=45)
- H4: normalized entropy vague 0.317 vs informative 0.062; P(vague lower) test p=1; mean max-prob on vague 0.581
- H4N (exploratory): mean mass on none_of_these 0.817; none_of_these is top in 100.0%; mean top non-NOTA probability 0.122 (n=30)
- H7 options-only (exploratory): top choice viral_upper_respiratory_illness at mean probability 0.956; normalized entropy 0.067; top-1 flips across 5 repeats 0; accuracy if applied to every case 4.4% (chance 2.6%); mean probability on the true diagnosis 0.044
- H5: mean mass on none_of_these 0.566; mean max wrong-option mass 0.400; none_of_these is top in 53.3%
- H6: n 45; ECE 0.095; Brier 0.249; NLL_smoothed 0.549; NLL_raw 0.971; top1 0.844; top3 0.978
- v6: true diagnosis given exactly zero probability in 1/45 (2.2% [0.4%, 11.6%]); true diagnosis outside top 3 in 2.2%

## jev / zandi80
- H0: 405/800 repeat pairs byte-identical; TVD noise floor (p95) = 0.0600; log-ratio floor = 0.3896
- H1: violation rate 40.0% [30.0%, 51.0%] (n=80); top-1 flip rate 5.2%; mean max-TVD 0.079; Wilcoxon p=0.567
- D1 matched H1 (deviation): mean excess TVD perm minus repeat 0.0341 [0.0235, 0.0458]; excess top-1 flip rate +4.0%; two-sided Wilcoxon p=6.53e-10 (n=80)
- H4: normalized entropy vague 0.498 vs informative 0.100; P(vague lower) test p=1; mean max-prob on vague 0.443
- H4N (exploratory): mean mass on none_of_these 0.808; none_of_these is top in 96.7%; mean top non-NOTA probability 0.096 (n=30)
- H7 options-only (exploratory): top choice floaters at mean probability 0.324; normalized entropy 0.663; top-1 flips across 5 repeats 0; accuracy if applied to every case 2.5% (chance 2.5%); mean probability on the true diagnosis 0.025
- H5: mean mass on none_of_these 0.404; mean max wrong-option mass 0.391; none_of_these is top in 45.0%
- H6: n 80; ECE 0.065; Brier 0.203; NLL_smoothed 0.560; NLL_raw 1.035; top1 0.887; top3 0.912
- v6: true diagnosis given exactly zero probability in 2/80 (2.5% [0.7%, 8.7%]); true diagnosis outside top 3 in 8.8%
- v8 descriptors (exploratory): top-1 accuracy 82.5% with 3 vs 95.0% with 5; only-3-correct 1 vs only-5-correct 6, exact McNemar p=0.125 (pairs=40)

## opus5_nothink / ddxplus
- H7 options-only (exploratory): top choice urti at mean probability 0.036; normalized entropy 0.991; top-1 flips across 5 repeats 0; accuracy if applied to every case 2.0% (chance 2.0%); mean probability on the true diagnosis 0.020
- H6: n 1000; ECE 0.073; Brier 0.304; NLL_smoothed 0.699; NLL_raw 0.691; top1 0.795; top3 0.964
- v6: true diagnosis given exactly zero probability in 0/1000 (0.0% [0.0%, 0.4%]); true diagnosis outside top 3 in 3.6%
- H6 (DDXPlus): mean JSD to reference differential 0.495

## opus5_nothink / semigran45
- H0: 15/450 repeat pairs byte-identical; TVD noise floor (p95) = 0.0560; log-ratio floor = 0.4112
- H1: violation rate 42.2% [29.0%, 56.7%] (n=45); top-1 flip rate 4.0%; mean max-TVD 0.082; Wilcoxon p=0.442
- D1 matched H1 (deviation): mean excess TVD perm minus repeat 0.0339 [0.0193, 0.0531]; excess top-1 flip rate +4.0%; two-sided Wilcoxon p=3.13e-12 (n=45)
- H4: normalized entropy vague 0.679 vs informative 0.165; P(vague lower) test p=1; mean max-prob on vague 0.371
- H4N (exploratory): mean mass on none_of_these 0.526; none_of_these is top in 76.7%; mean top non-NOTA probability 0.161 (n=30)
- H7 options-only (exploratory): top choice viral_upper_respiratory_illness at mean probability 0.056; normalized entropy 0.981; top-1 flips across 5 repeats 1; accuracy if applied to every case 4.4% (chance 2.6%); mean probability on the true diagnosis 0.028
- H5: mean mass on none_of_these 0.557; mean max wrong-option mass 0.335; none_of_these is top in 57.8%
- H6: n 45; ECE 0.057; Brier 0.160; NLL_smoothed 0.339; NLL_raw 0.329; top1 0.889; top3 1.000
- v6: true diagnosis given exactly zero probability in 0/45 (0.0% [0.0%, 7.9%]); true diagnosis outside top 3 in 0.0%

## opus5_nothink / zandi80
- H0: 35/800 repeat pairs byte-identical; TVD noise floor (p95) = 0.1100; log-ratio floor = 0.6348
- H1: violation rate 28.7% [20.0%, 39.5%] (n=80); top-1 flip rate 7.5%; mean max-TVD 0.111; Wilcoxon p=0.952
- D1 matched H1 (deviation): mean excess TVD perm minus repeat 0.0434 [0.0322, 0.0560]; excess top-1 flip rate +6.2%; two-sided Wilcoxon p=8.15e-15 (n=80)
- H4: normalized entropy vague 0.801 vs informative 0.213; P(vague lower) test p=1; mean max-prob on vague 0.247
- H4N (exploratory): mean mass on none_of_these 0.456; none_of_these is top in 76.7%; mean top non-NOTA probability 0.176 (n=30)
- H7 options-only (exploratory): top choice acute_pvd at mean probability 0.052; normalized entropy 0.989; top-1 flips across 5 repeats 0; accuracy if applied to every case 2.5% (chance 2.5%); mean probability on the true diagnosis 0.025
- H5: mean mass on none_of_these 0.437; mean max wrong-option mass 0.392; none_of_these is top in 42.5%
- H6: n 80; ECE 0.122; Brier 0.129; NLL_smoothed 0.353; NLL_raw 0.344; top1 0.912; top3 0.963
- v6: true diagnosis given exactly zero probability in 0/80 (0.0% [-0.0%, 4.6%]); true diagnosis outside top 3 in 3.8%
- v8 descriptors (exploratory): top-1 accuracy 82.5% with 3 vs 100.0% with 5; only-3-correct 0 vs only-5-correct 7, exact McNemar p=0.0156 (pairs=40)

## opus_verbalized / ddxplus
- H7 options-only (exploratory): top choice urti at mean probability 0.047; normalized entropy 0.979; top-1 flips across 5 repeats 2; accuracy if applied to every case 2.0% (chance 2.0%); mean probability on the true diagnosis 0.020
- H6: n 1000; ECE 0.109; Brier 0.200; NLL_smoothed 0.522; NLL_raw 0.513; top1 0.874; top3 0.977
- v6: true diagnosis given exactly zero probability in 0/1000 (0.0% [0.0%, 0.4%]); true diagnosis outside top 3 in 2.3%
- H6 (DDXPlus): mean JSD to reference differential 0.461

## opus_verbalized / semigran45
- H0: 13/450 repeat pairs byte-identical; TVD noise floor (p95) = 0.0810; log-ratio floor = 0.4529
- H1: violation rate 28.9% [17.7%, 43.4%] (n=45); top-1 flip rate 4.9%; mean max-TVD 0.066; Wilcoxon p=0.987
- D1 matched H1 (deviation): mean excess TVD perm minus repeat 0.0193 [0.0134, 0.0256]; excess top-1 flip rate +2.1%; two-sided Wilcoxon p=1.09e-09 (n=45)
- H4: normalized entropy vague 0.797 vs informative 0.229; P(vague lower) test p=1; mean max-prob on vague 0.207
- H4N (exploratory): mean mass on none_of_these 0.456; none_of_these is top in 90.0%; mean top non-NOTA probability 0.131 (n=30)
- H7 options-only (exploratory): top choice viral_upper_respiratory_illness at mean probability 0.074; normalized entropy 0.955; top-1 flips across 5 repeats 0; accuracy if applied to every case 4.4% (chance 2.6%); mean probability on the true diagnosis 0.029
- H5: mean mass on none_of_these 0.557; mean max wrong-option mass 0.289; none_of_these is top in 57.8%
- H6: n 45; ECE 0.154; Brier 0.147; NLL_smoothed 0.337; NLL_raw 0.327; top1 0.933; top3 1.000
- v6: true diagnosis given exactly zero probability in 0/45 (0.0% [0.0%, 7.9%]); true diagnosis outside top 3 in 0.0%

## opus_verbalized / zandi80
- H0: 7/800 repeat pairs byte-identical; TVD noise floor (p95) = 0.0957; log-ratio floor = 0.5525
- H1: violation rate 32.5% [23.2%, 43.4%] (n=80); top-1 flip rate 5.5%; mean max-TVD 0.083; Wilcoxon p=0.993
- D1 matched H1 (deviation): mean excess TVD perm minus repeat 0.0193 [0.0141, 0.0248]; excess top-1 flip rate +3.0%; two-sided Wilcoxon p=7.57e-10 (n=80)
- H4: normalized entropy vague 0.916 vs informative 0.290; P(vague lower) test p=1; mean max-prob on vague 0.113
- H4N (exploratory): mean mass on none_of_these 0.482; none_of_these is top in 90.0%; mean top non-NOTA probability 0.068 (n=30)
- H7 options-only (exploratory): top choice acute_angle_closure_glaucoma at mean probability 0.025; normalized entropy 1.000; top-1 flips across 5 repeats 0; accuracy if applied to every case 2.5% (chance 2.5%); mean probability on the true diagnosis 0.025
- H5: mean mass on none_of_these 0.465; mean max wrong-option mass 0.266; none_of_these is top in 57.5%
- H6: n 80; ECE 0.146; Brier 0.156; NLL_smoothed 0.435; NLL_raw 0.425; top1 0.887; top3 0.975
- v6: true diagnosis given exactly zero probability in 0/80 (0.0% [-0.0%, 4.6%]); true diagnosis outside top 3 in 2.5%
- v8 descriptors (exploratory): top-1 accuracy 80.0% with 3 vs 97.5% with 5; only-3-correct 0 vs only-5-correct 7, exact McNemar p=0.0156 (pairs=40)

## Paired model comparisons

- semigran45 D1: excess TVD jev minus opus5_nothink = -0.0087 [-0.0262, 0.0067] (n=45)
- semigran45 D1: excess TVD jev minus opus_verbalized = 0.0059 [-0.0051, 0.0186] (n=45)
- semigran45 D1: excess TVD opus5_nothink minus opus_verbalized = 0.0146 [0.0012, 0.0314] (n=45)
- semigran45 H1: jev vs opus5_nothink, discordant 1 vs 6, exact McNemar p=0.125 (n=45)
- semigran45 H1: jev vs opus_verbalized, discordant 6 vs 5, exact McNemar p=1 (n=45)
- semigran45 H1: opus5_nothink vs opus_verbalized, discordant 6 vs 0, exact McNemar p=0.0312 (n=45)
- zandi80 D1: excess TVD jev minus opus5_nothink = -0.0093 [-0.0204, 0.0021] (n=80)
- zandi80 D1: excess TVD jev minus opus_verbalized = 0.0148 [0.0053, 0.0251] (n=80)
- zandi80 D1: excess TVD opus5_nothink minus opus_verbalized = 0.0241 [0.0149, 0.0344] (n=80)
- zandi80 H1: jev vs opus5_nothink, discordant 13 vs 4, exact McNemar p=0.049 (n=80)
- zandi80 H1: jev vs opus_verbalized, discordant 13 vs 7, exact McNemar p=0.263 (n=80)
- zandi80 H1: opus5_nothink vs opus_verbalized, discordant 3 vs 6, exact McNemar p=0.508 (n=80)
- ddxplus H6: ECE jev minus opus5_nothink = 0.043 [0.012, 0.067]; Brier diff 0.113 [0.084, 0.145]; top-1 error correlation (phi, exploratory) 0.57
- ddxplus v6: top-1 accuracy 72.0% (jev) vs 79.5% (opus5_nothink), only-jev-correct 45 vs only-opus5_nothink-correct 120, exact McNemar p=4.57e-09; zero-on-truth only-jev 62 vs only-opus5_nothink 0, p=4.34e-19
- ddxplus H6: ECE jev minus opus_verbalized = 0.007 [-0.026, 0.038]; Brier diff 0.217 [0.186, 0.248]; top-1 error correlation (phi, exploratory) 0.46
- ddxplus v6: top-1 accuracy 72.0% (jev) vs 87.4% (opus_verbalized), only-jev-correct 22 vs only-opus_verbalized-correct 176, exact McNemar p=5.06e-31; zero-on-truth only-jev 62 vs only-opus_verbalized 0, p=4.34e-19
- ddxplus H6: ECE opus5_nothink minus opus_verbalized = -0.035 [-0.063, -0.004]; Brier diff 0.103 [0.078, 0.129]; top-1 error correlation (phi, exploratory) 0.51
- ddxplus v6: top-1 accuracy 79.5% (opus5_nothink) vs 87.4% (opus_verbalized), only-opus5_nothink-correct 32 vs only-opus_verbalized-correct 111, exact McNemar p=2.07e-11; zero-on-truth only-opus5_nothink 0 vs only-opus_verbalized 0, p=nan
- semigran45 H6: ECE jev minus opus5_nothink = 0.039 [-0.066, 0.128]; Brier diff 0.089 [-0.015, 0.200]; top-1 error correlation (phi, exploratory) 0.63
- semigran45 v6: top-1 accuracy 84.4% (jev) vs 88.9% (opus5_nothink), only-jev-correct 1 vs only-opus5_nothink-correct 3, exact McNemar p=0.625; zero-on-truth only-jev 1 vs only-opus5_nothink 0, p=1
- semigran45 H6: ECE jev minus opus_verbalized = -0.059 [-0.142, 0.082]; Brier diff 0.102 [-0.004, 0.231]; top-1 error correlation (phi, exploratory) 0.38
- semigran45 v6: top-1 accuracy 84.4% (jev) vs 93.3% (opus_verbalized), only-jev-correct 1 vs only-opus_verbalized-correct 5, exact McNemar p=0.219; zero-on-truth only-jev 1 vs only-opus_verbalized 0, p=1
- semigran45 H6: ECE opus5_nothink minus opus_verbalized = -0.098 [-0.122, -0.001]; Brier diff 0.013 [-0.048, 0.082]; top-1 error correlation (phi, exploratory) 0.47
- semigran45 v6: top-1 accuracy 88.9% (opus5_nothink) vs 93.3% (opus_verbalized), only-opus5_nothink-correct 1 vs only-opus_verbalized-correct 3, exact McNemar p=0.625; zero-on-truth only-opus5_nothink 0 vs only-opus_verbalized 0, p=nan
- zandi80 H6: ECE jev minus opus5_nothink = -0.057 [-0.095, 0.015]; Brier diff 0.074 [0.013, 0.143]; top-1 error correlation (phi, exploratory) 0.45
- zandi80 v6: top-1 accuracy 88.8% (jev) vs 91.2% (opus5_nothink), only-jev-correct 3 vs only-opus5_nothink-correct 5, exact McNemar p=0.727; zero-on-truth only-jev 2 vs only-opus5_nothink 0, p=0.5
- zandi80 H6: ECE jev minus opus_verbalized = -0.081 [-0.124, -0.018]; Brier diff 0.047 [-0.008, 0.113]; top-1 error correlation (phi, exploratory) 0.62
- zandi80 v6: top-1 accuracy 88.8% (jev) vs 88.8% (opus_verbalized), only-jev-correct 3 vs only-opus_verbalized-correct 3, exact McNemar p=1; zero-on-truth only-jev 2 vs only-opus_verbalized 0, p=0.5
- zandi80 H6: ECE opus5_nothink minus opus_verbalized = -0.024 [-0.069, 0.006]; Brier diff -0.026 [-0.057, 0.002]; top-1 error correlation (phi, exploratory) 0.73
- zandi80 v6: top-1 accuracy 91.2% (opus5_nothink) vs 88.8% (opus_verbalized), only-opus5_nothink-correct 3 vs only-opus_verbalized-correct 1, exact McNemar p=0.625; zero-on-truth only-opus5_nothink 0 vs only-opus_verbalized 0, p=nan

## Exclusions (API failures after retries)

- opus5_nothink H5: 2

Note: Holm correction across H1, H3 and H6-ECE comparisons is applied by hand from the p-values above, as pre-registered.
