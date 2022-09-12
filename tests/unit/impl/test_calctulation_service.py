from hamcrest import assert_that, equal_to, has_properties, instance_of, has_length

from multibar import iterators
from multibar.impl.calculation_service import ProgressbarCalculationService


def test_percentage() -> None:
    percentage = ProgressbarCalculationService.get_progress_percentage(50, 100)
    assert_that(percentage, equal_to(50.0))


def test_calculation_service() -> None:
    calc_service = ProgressbarCalculationService(50, 100, 20)

    assert_that(
        calc_service,
        has_properties(
            {
                "start_value": equal_to(50),
                "end_value": equal_to(100),
                "length_value": equal_to(20),
                "progress_percents": equal_to(50.0),
            }
        )
    )

    first_part = calc_service.calculate_filled_indexes()
    second_part = calc_service.calculate_unfilled_indexes()

    assert_that(first_part, instance_of(iterators.AbstractIterator))
    assert_that(second_part, instance_of(iterators.AbstractIterator))

    assert_that(list(first_part), has_length(calc_service.length_value // 2))
    assert_that(list(second_part), has_length(calc_service.length_value // 2))
