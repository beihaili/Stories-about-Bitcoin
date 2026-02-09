import { renderHook, act } from '@testing-library/react'
import useTheme from '../useTheme'

describe('useTheme', () => {
  it('defaults to light when no stored value and system prefers light', () => {
    const { result } = renderHook(() => useTheme())
    expect(result.current.theme).toBe('light')
  })

  it('reads stored theme from localStorage', () => {
    localStorage.setItem('theme', 'dark')
    const { result } = renderHook(() => useTheme())
    expect(result.current.theme).toBe('dark')
  })

  it('toggleTheme switches dark to light', () => {
    localStorage.setItem('theme', 'dark')
    const { result } = renderHook(() => useTheme())
    act(() => result.current.toggleTheme())
    expect(result.current.theme).toBe('light')
  })

  it('toggleTheme switches light to dark', () => {
    const { result } = renderHook(() => useTheme())
    expect(result.current.theme).toBe('light')
    act(() => result.current.toggleTheme())
    expect(result.current.theme).toBe('dark')
  })

  it('adds dark class to documentElement when dark', () => {
    localStorage.setItem('theme', 'dark')
    renderHook(() => useTheme())
    expect(document.documentElement.classList.contains('dark')).toBe(true)
  })

  it('removes dark class when light', () => {
    document.documentElement.classList.add('dark')
    localStorage.setItem('theme', 'light')
    renderHook(() => useTheme())
    expect(document.documentElement.classList.contains('dark')).toBe(false)
  })

  it('persists theme to localStorage on toggle', () => {
    const { result } = renderHook(() => useTheme())
    act(() => result.current.toggleTheme())
    expect(localStorage.getItem('theme')).toBe('dark')
  })
})
