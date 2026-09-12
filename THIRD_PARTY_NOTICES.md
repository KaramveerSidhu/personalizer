# Third-party notices

## Humanizer foundation

The structural cleanup guidance and preservation approach in `references/humanizer-core.md` and the writing workflow are adapted from [blader/humanizer](https://github.com/blader/humanizer), version 3.0.0, inspected on 2026-09-12 at commit [`9862685f575c65a8247f90369951df1b3416e3d6`](https://github.com/blader/humanizer/tree/9862685f575c65a8247f90369951df1b3416e3d6). The catalog has been condensed and rewritten for this skill. Personalizer deliberately changes generic punctuation defaults, profile persistence, and output behavior. No upstream before/after examples are bundled.

Humanizer's complete MIT notice follows:

```text
MIT License

Copyright (c) 2025 Siqi Chen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Humanize inspiration

[shir-danishyar/humanize](https://github.com/shir-danishyar/humanize), formerly `Shirhussain/humanize`, was inspected on 2026-09-12 at commit [`024aa193966341e0706e96f0277f914092bed2c7`](https://github.com/shir-danishyar/humanize/tree/024aa193966341e0706e96f0277f914092bed2c7). It inspired the separation of calibration, generation/rewrite, and register-sensitive profile application. Its code, voice template, vocabulary lists, sample excerpts and pattern catalog were not copied. Its MIT notice is retained here for clear attribution:

```text
MIT License

Copyright (c) 2026 Shirhussain Danishyar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

## Original work

Personalizer's profile schema, private storage and lookup rules, evidence/confidence and update model, voice-matching instructions, Python metrics helper, and synthetic tests were independently implemented. These additions use the MIT license in `LICENSE.txt`. No active author profile or genuine writing sample is part of this package.

The upstream projects cite Wikipedia's Signs of AI writing as background. This package does not reproduce Wikipedia text or its examples. Future additions copied from other sources need their own attribution review.
