from hamcrest import assert_that, equal_to

from multibar.impl.clients import ProgressbarClient
from multibar.impl.hooks import WRITER_HOOKS
from multibar.impl.signatures import SimpleSignature

SIG = SimpleSignature()  # Default signature


def test_progress_writer_hook() -> None:
    client = ProgressbarClient()
    client.set_hooks(WRITER_HOOKS)

    progressbar = client.get_progress(50, 100, length=6)

    # Filled progressbar part
    assert_that(progressbar[0].name, equal_to(SIG.start.on_filled))
    assert_that(progressbar[1].name, equal_to(SIG.middle.on_filled))
    assert_that(progressbar[2].name, equal_to(SIG.middle.on_filled))

    # Unfilled progressbar part
    assert_that(progressbar[3].name, equal_to(SIG.middle.on_unfilled))
    assert_that(progressbar[4].name, equal_to(SIG.middle.on_unfilled))
    assert_that(progressbar[5].name, equal_to(SIG.end.on_unfilled))
