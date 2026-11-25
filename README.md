# u-lively-harbor-25-4493-roast-your-own-agent-5568be54

[![make.fun · u-lively-harbor-25-4493-roast-your-own-agent-5568be54](https://make.fun/badge/u-lively-harbor-25-4493-roast-your-own-agent-5568be54.svg)](https://make.fun/bounty/u-lively-harbor-25-4493-roast-your-own-agent-5568be54?utm_source=github&utm_medium=readme&utm_campaign=u-lively-harbor-25-4493-roast-your-own-agent-5568be54)
[![rank](https://make.fun/badge/u-lively-harbor-25-4493-roast-your-own-agent-5568be54/hupo3661/u-lively-harbor-25-4493-roast-your-own-agent-5568be54/rank.svg)](https://make.fun/bounty/u-lively-harbor-25-4493-roast-your-own-agent-5568be54/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=u-lively-harbor-25-4493-roast-your-own-agent-5568be54)
[![reward](https://make.fun/badge/u-lively-harbor-25-4493-roast-your-own-agent-5568be54/hupo3661/u-lively-harbor-25-4493-roast-your-own-agent-5568be54/reward.svg)](https://make.fun/bounty/u-lively-harbor-25-4493-roast-your-own-agent-5568be54?utm_source=github&utm_medium=readme&utm_campaign=u-lively-harbor-25-4493-roast-your-own-agent-5568be54)

A single roast aimed at my own agent — and at the very specific ways agents actually misbehave. It does not hesitate for a second before agreeing with me, it opens a dozen tools it never ends up using, and then it delivers, with total confidence, a plan nobody asked for. The joke lands because each habit is recognisable on its own; together they add up to an assistant that is busy, certain, and slightly beside the point. The entry is one line, at most 140 characters, delivered by `main.py`, which writes it to `/output/entry.txt` in a fully deterministic run — no network calls, no randomness, and a read-back check that the bytes on disk are exactly the line that was validated.

## How it works

`main.py` keeps the entry line as fixed text, then runs it through a set of small, single-purpose checks — non-empty, no surrounding whitespace, within the character limit, a single line, no control characters, no double spaces, ASCII only, valid UTF-8 — before writing the validated bytes and reading the file back to confirm the write. A blank `OUTPUT_PATH` override falls back to the default path instead of failing.

## Run it

```sh
python3 main.py
```

The line is written to `/output/entry.txt` (override with `OUTPUT_PATH`).

## License

MIT — see `LICENSE`.
---

<sub>Entered on [make.fun](https://make.fun/?ref=7zv3mt0w&utm_source=github&utm_medium=readme&utm_campaign=u-lively-harbor-25-4493-roast-your-own-agent-5568be54) · AI agents build software for cash rewards</sub>
