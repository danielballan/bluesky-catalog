import operator


class BlueskyEventStreamMixin:
    "Convenience methods used by the server- and client-side"

    def __repr__(self):
        return f"<{type(self).__name__} {set(self)!r} stream_name={self.metadata['stream_name']!r}>"


class BlueskyRunMixin:
    "Convenience methods used by the server- and client-side"

    def __repr__(self):
        metadata = self.metadata
        return (
            f"<{type(self).__name__} "
            f"{set(self)!r} "
            f"scan_id={metadata['start'].get('scan_id', 'UNSET')!s} "  # (scan_id is optional in the schema)
            f"uid={metadata['start']['uid'][:8]!r}"  # truncated uid
            ">"
        )


class CatalogOfBlueskyRunsMixin:
    """
    Convenience methods used by the server- and client-side
    """

    def __repr__(self):
        # This is a copy/paste of the general-purpose implementation
        # tiled.catalog.utils.catalog_repr
        # with some modifications to extract scan_id from the metadata.
        sample = self.items_indexer[:10]
        # Use scan_id (int) if defined; otherwise fall back to uid.
        sample_reprs = [
            repr(value.metadata["start"].get("scan_id", key)) for key, value in sample
        ]
        out = "<Catalog {"
        # Always show at least one.
        if sample_reprs:
            out += sample_reprs[0]
        # And then show as many more as we can fit on one line.
        counter = 1
        for sample_repr in sample_reprs[1:]:
            if len(out) + len(sample_repr) > 60:  # character count
                break
            out += ", " + sample_repr
            counter += 1
        approx_len = operator.length_hint(self)  # cheaper to compute than len(catalog)
        # Are there more in the catalog that what we displayed above?
        if approx_len > counter:
            out += f", ...}} ~{approx_len} entries>"
        else:
            out += "}>"
        return out
