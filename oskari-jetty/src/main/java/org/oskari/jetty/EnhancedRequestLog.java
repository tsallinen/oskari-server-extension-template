package org.oskari.jetty;

import ch.qos.logback.access.jetty.RequestLogImpl;
import org.eclipse.jetty.util.component.LifeCycle;

// Workaround to:
// https://github.com/eclipse/jetty.project/issues/509
// https://github.com/qos-ch/logback/pull/269
public class EnhancedRequestLog extends RequestLogImpl implements LifeCycle {
}
