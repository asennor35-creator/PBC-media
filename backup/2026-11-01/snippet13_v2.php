// Link WA berkode: pratamabuild.id/wa/K013 -> WhatsApp PBC dengan kode sumber, klik dicatat di pbc_wa_clicks (wa-k013)
add_action( 'template_redirect', function () {
	$path = trim( (string) parse_url( $_SERVER['REQUEST_URI'], PHP_URL_PATH ), '/' );
	if ( ! preg_match( '#^wa/([A-Za-z0-9-]{1,20})$#', $path, $m ) ) { return; }
	$code = strtoupper( $m[1] );
	if ( 0 !== strpos( $code, 'UJI' ) ) {
		$ip  = isset( $_SERVER['REMOTE_ADDR'] ) ? $_SERVER['REMOTE_ADDR'] : '';
		$key = 'pbc_wak_' . md5( $ip . $code );
		if ( ! get_transient( $key ) ) {
			set_transient( $key, 1, 30 );
			$src = 'wa-' . sanitize_key( $code );
			$day = current_time( 'Y-m-d' );
			$all = get_option( 'pbc_wa_clicks', array() );
			if ( ! is_array( $all ) ) { $all = array(); }
			if ( ! isset( $all[ $day ] ) ) { $all[ $day ] = array(); }
			$all[ $day ][ $src ] = ( isset( $all[ $day ][ $src ] ) ? $all[ $day ][ $src ] : 0 ) + 1;
			update_option( 'pbc_wa_clicks', $all, false );
		}
	}
	do_action( 'litespeed_control_set_nocache', 'pbc wa kode' );
	nocache_headers();
	$text = rawurlencode( 'Halo PBC, saya mau tanya soal proyek. (' . $code . ')' );
	wp_redirect( 'https://wa.me/6285745026574?text=' . $text, 302 );
	exit;
}, 5 );

// Dasbor wp-admin: klik WA per kode (berjalan tanpa Claude)
add_action( 'wp_dashboard_setup', function () {
	if ( ! current_user_can( 'manage_options' ) ) { return; }
	wp_add_dashboard_widget( 'pbc_wa_kode', 'PBC: Klik WhatsApp per kode (30 hari)', function () {
		$all = get_option( 'pbc_wa_clicks', array() );
		$from = gmdate( 'Y-m-d', strtotime( '-30 days' ) );
		$sum = array(); $days = array();
		foreach ( (array) $all as $day => $row ) {
			if ( $day < $from ) { continue; }
			foreach ( (array) $row as $k => $n ) {
				if ( 0 !== strpos( $k, 'wa-' ) || 0 === strpos( $k, 'wa-syscheck' ) ) { continue; }
				$c = strtoupper( substr( $k, 3 ) );
				$sum[ $c ] = ( isset( $sum[ $c ] ) ? $sum[ $c ] : 0 ) + $n;
				$days[ $c ] = $day;
			}
		}
		arsort( $sum );
		if ( ! $sum ) { echo '<p>Belum ada klik link WA berkode.</p>'; return; }
		echo '<table class="widefat striped"><thead><tr><th>Kode</th><th>Klik</th><th>Klik terakhir</th></tr></thead><tbody>';
		foreach ( $sum as $c => $n ) { echo '<tr><td>' . esc_html( $c ) . '</td><td>' . (int) $n . '</td><td>' . esc_html( $days[ $c ] ) . '</td></tr>'; }
		echo '</tbody></table><p style="color:#666">Klik = orang membuka link. Pesan & lead dicatat di PBC Marketing Hub.</p>';
	} );
} );
