from hamcrest import assert_that, instance_of

from multibar.impl.calculation_service import ProgressbarCalculationService
from multibar.impl.progressbars import Progressbar
from multibar.impl.sectors import Sector
from multibar.impl.signatures import SimpleSignature
from multibar.impl.writers import ProgressbarWriter
from tests.impl.calculation_service import FakeCalculationService
from tests.impl.progressbars import FakeProgressbar
from tests.impl.sectors import FakeSector
from tests.impl.signatures import FakeSignature
from tests.pyhamcrest import subclass_of


class TestProgressWriterConfiguration:
    def test_base(self) -> None:
        default_writer_state = ProgressbarWriter()

        # ProgressWriter base tested on tests/unit/impl/progressbars.py
        assert_that(default_writer_state.sector_cls, subclass_of(Sector))
        assert_that(default_writer_state.calculation_cls, subclass_of(ProgressbarCalculationService))
        assert_that(default_writer_state.signature, instance_of(SimpleSignature))

        # Setting new configuration
        custom_writer_state = ProgressbarWriter(
            sector_cls=FakeSector,
            progressbar_cls=FakeProgressbar,
            signature=FakeSignature(),
            calculation_service=FakeCalculationService,
        )

        assert_that(custom_writer_state.progressbar_cls, subclass_of(FakeProgressbar))
        assert_that(custom_writer_state.sector_cls, subclass_of(FakeSector))
        assert_that(custom_writer_state.calculation_cls, subclass_of(FakeCalculationService))
        assert_that(custom_writer_state.signature, instance_of(FakeSignature))

    def test_write_progress(self) -> None:
        writer_state = ProgressbarWriter()
        progressbar = writer_state.write(50, 100)

        assert_that(progressbar, instance_of(Progressbar))
