def find_element_with_fallback(page, strategies, logger):
    for i, (strategy, value) in enumerate(strategies):
        try:
            if strategy == "placeholder":
                element = page.get_by_placeholder(value)
            elif strategy == "id":
                element = page.locator(f"#{value}")
            elif strategy == "class":
                element = page.locator(f".{value}")
            elif strategy == "text":
                element = page.get_by_text(value)
            elif strategy == "css":
                element = page.locator(value)
            elif strategy == "xpath":
                element = page.locator(value)
            elif strategy == "data-test":
                element = page.locator(value)
            else:
                continue

            if element.is_visible():
                if i > 0:  # Log only if we are not using the first locator
                    logger.warning(f"Primary locator failed. Using alternate locator: {strategy}='{value}'")
                return element
        except Exception as e:
            logger.debug(f"Locator {strategy}='{value}' failed: {e}")
            continue
    raise Exception("None of the locators were successful")