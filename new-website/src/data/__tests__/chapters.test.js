import { existsSync } from 'node:fs'
import { basename, join } from 'node:path'
import { cwd } from 'node:process'
import { chapters, periods } from '../chapters'

const repoRoot = join(cwd(), '..')

describe('chapter data integrity', () => {
  it('contains 39 chapters across 9 periods', () => {
    expect(chapters).toHaveLength(39)
    expect(periods).toHaveLength(9)
  })

  it.each(['zh', 'en'])('has an existing %s target for every chapter', (lang) => {
    const sourceDirectory = lang === 'zh' ? '正文' : 'en'

    for (const chapter of chapters) {
      const link = chapter.link[lang]
      expect(link, `chapter ${chapter.id} ${lang} link`).toBeTruthy()

      const sourceName = basename(link).replace(/\.html$/, '.md')
      expect(
        existsSync(join(repoRoot, sourceDirectory, sourceName)),
        `missing source for ${link}`,
      ).toBe(true)
    }
  })
})
