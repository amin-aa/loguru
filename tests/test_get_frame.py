import sys
import pytest
import loguru

def test_with_sys_getframe(monkeypatch):
    patched = lambda: None
    monkeypatch.setattr(sys, '_getframe', patched)
    assert loguru.get_getframe_function() == patched

def test_without_sys_getframe(monkeypatch):
    monkeypatch.delattr(sys, '_getframe')
    assert loguru.get_getframe_function() == loguru.getframe_fallback

def test_getframe_fallback():
    frame_root = frame_a = frame_b = None

    def a():
        nonlocal frame_a
        frame_a = loguru.getframe_fallback(1)
        b()

    def b():
        nonlocal frame_b
        frame_b = loguru.getframe_fallback(2)

    frame_root = loguru.getframe_fallback(0)
    a()

    assert frame_a == frame_b == frame_root
