from unittest.mock import Mock

from hamcrest import assert_that, has_properties, instance_of, is_, is_not

from multibar.api.writers import ProgressbarWriterAware
from multibar.impl.writers import ProgressbarWriter
from tests.pyhamcrest import subclass_of


class TestProgressbarWriter:
    def test_base(self) -> None:
        writer_state = ProgressbarWriter()

        assert_that(ProgressbarWriter, subclass_of(ProgressbarWriterAware))
        assert_that(
            writer_state,
            has_properties(
                {
                    "signature": is_not(None),
                    "sector_cls": is_not(None),
                    "progressbar_cls": is_not(None),
                    "calculation_cls": is_not(None),
                },
            ),
        )

    def test_alternative_constructors(self) -> None:
        writer_state = ProgressbarWriter.from_signature(Mock())
        assert_that(writer_state, instance_of(ProgressbarWriter))

    def test_bind_signature(self) -> ProgressbarWriter:
        writer_state = ProgressbarWriter()
        mock_signature = Mock()

        assert_that(writer_state.signature, is_not(mock_signature))

        writer_state.bind_signature(mock_signature)
        assert_that(writer_state.signature, is_(mock_signature))
