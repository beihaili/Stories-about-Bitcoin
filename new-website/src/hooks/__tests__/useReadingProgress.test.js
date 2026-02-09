import { renderHook, act } from '@testing-library/react'
import useReadingProgress from '../useReadingProgress'

describe('useReadingProgress', () => {
  it('starts with empty reading list', () => {
    const { result } = renderHook(() => useReadingProgress())
    expect(result.current.readChapters).toEqual([])
    expect(result.current.readCount).toBe(0)
  })

  it('restores from localStorage', () => {
    localStorage.setItem('readChapters', JSON.stringify([1, 5, 10]))
    const { result } = renderHook(() => useReadingProgress())
    expect(result.current.readChapters).toEqual([1, 5, 10])
    expect(result.current.readCount).toBe(3)
  })

  it('markAsRead adds a chapter', () => {
    const { result } = renderHook(() => useReadingProgress())
    act(() => result.current.markAsRead(7))
    expect(result.current.readChapters).toEqual([7])
    expect(result.current.readCount).toBe(1)
  })

  it('markAsRead does not add duplicates', () => {
    const { result } = renderHook(() => useReadingProgress())
    act(() => result.current.markAsRead(3))
    act(() => result.current.markAsRead(3))
    expect(result.current.readChapters).toEqual([3])
    expect(result.current.readCount).toBe(1)
  })

  it('isRead returns true for read chapters', () => {
    const { result } = renderHook(() => useReadingProgress())
    act(() => result.current.markAsRead(12))
    expect(result.current.isRead(12)).toBe(true)
    expect(result.current.isRead(13)).toBe(false)
  })

  it('persists to localStorage on markAsRead', () => {
    const { result } = renderHook(() => useReadingProgress())
    act(() => result.current.markAsRead(1))
    act(() => result.current.markAsRead(2))
    expect(JSON.parse(localStorage.getItem('readChapters'))).toEqual([1, 2])
  })

  it('handles corrupted localStorage gracefully', () => {
    localStorage.setItem('readChapters', 'not-json')
    const { result } = renderHook(() => useReadingProgress())
    expect(result.current.readChapters).toEqual([])
  })
})
